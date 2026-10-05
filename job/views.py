from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
import traceback
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages


def index(request):
    return render(request,'index.html')

def user_home(request):

    if not request.user.is_authenticated:
        return redirect('user_login')

    try:
        student = StudentUser.objects.get(user=request.user)
    except StudentUser.DoesNotExist:
        return redirect('user_login')

    error = None

    if request.method == "POST":

        try:
            # Form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            gender = request.POST.get('gender')

            # Update User table
            student.user.first_name = name
            student.user.email = email
            student.user.save()

            # Update StudentUser table
            student.mobile = mobile
            student.gender = gender

            # Update image
            if request.FILES.get('image'):
                student.image = request.FILES.get('image')

            student.save()

            error = "no"

        except Exception as e:
            print("USER PROFILE UPDATE ERROR:", e)
            error = "yes"

    return render(request, 'user_home.html', {
        'student': student,
        'error': error
    })

def recruiter_home(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')
    return render(request,'recruiter_home.html')

def Logout(request):
    logout(request)
    return redirect('index')

def admin_login(request):
    error = ""

    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')

        user = authenticate(username=u, password=p)

        if user is not None:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        else:
            error = "yes"

    d = {'error': error}
    return render(request, 'admin_login.html', d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request,'admin_home.html')

def recruiter_home(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    try:
        recruiter = Recruiter.objects.get(user=request.user)
    except Recruiter.DoesNotExist:
        return redirect('recruiter_login')

    error = None

    if request.method == "POST":

        try:
            # Form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            company = request.POST.get('company')
            gender = request.POST.get('gender')

            # Update User table
            recruiter.user.first_name = name
            recruiter.user.email = email
            recruiter.user.save()

            # Update Recruiter table
            recruiter.mobile = mobile
            recruiter.company = company
            recruiter.gender = gender

            # Update image if selected
            if request.FILES.get('image'):
                recruiter.image = request.FILES.get('image')

            recruiter.save()

            error = "no"

        except Exception as e:
            print("PROFILE UPDATE ERROR:", e)
            error = "yes"

    return render(request, 'recruiter_home.html', {
        'recruiter': recruiter,
        'error': error
    })

def user_login(request):
    error = ""

    if request.method == "POST":
        u = request.POST.get('uname')
        p = request.POST.get('pwd')

        user = authenticate(username=u, password=p)

        if user is not None:
            try:
                user1 = StudentUser.objects.get(user=user)

                if user1.type == "student":
                    login(request, user)
                    error = "no"
                else:
                    error = "yes"

            except StudentUser.DoesNotExist:
                error = "yes"

        else:
            error = "yes"

    return render(request, 'user_login.html', {'error': error})

def recruiter_login(request):
    error = ""
   
    if request.method == "POST":
           u = request.POST.get('uname')
           p = request.POST.get('pwd')
   
           user = authenticate(username=u, password=p)
   
           if user is not None:
               try:
                   user1 = Recruiter.objects.get(user=user)
   
                   if user1.type == "recruiter" and user1.status != "pending":
                       login(request, user)
                       error = "no"
                   else:
                       error = "not"
   
               except Recruiter.DoesNotExist:
                   error = "yes"
   
           else:
               error = "yes"
   
    return render(request, 'recruiter_login.html', {'error': error})

def recruiter_signup(request):
    error = ""
    
    if request.method == "POST":
        f = request.POST.get('name')
        em = request.POST.get('email')
        m = request.POST.get('mobile')
        g = request.POST.get('gender')
        i = request.FILES.get('image')  
        p = request.POST.get('pwd')
        com = request.POST.get('company')
        
    
        try:
                # Create Django User
            user = User.objects.create_user(
                    username=em,
                    email=em,
                    password=p,
                    first_name=f
                )
    
                # Create Student Profile
            Recruiter.objects.create(
                    user=user,
                    mobile=m,
                    image=i,
                    gender=g,
                    company=com,
                    type="recruiter",
                    status="pending"
                )
    
            error = "no"
    
        except Exception as e:
            
            print("ERROR:", e)
        
            traceback.print_exc()
            error = "yes"
    return render(request, 'recruiter_signup.html', {"error": error})

def user_signup(request):
    error = ""

    if request.method == "POST":
        f = request.POST.get('name')
        em = request.POST.get('email')
        m = request.POST.get('mobile')
        g = request.POST.get('gender')
        i = request.FILES.get('image')  
        p = request.POST.get('pwd')

        try:
            # Create Django User
            user = User.objects.create_user(
                username=em,
                email=em,
                password=p,
                first_name=f
            )

            # Create Student Profile
            StudentUser.objects.create(
                user=user,
                mobile=m,
                image=i,
                gender=g,
                type="student"
            )

            error = "no"

        except Exception as e:
           print("ERROR:", e)
    
           traceback.print_exc()
           error = "yes"
    return render(request, "user_signup.html", {"error": error})

def admin_signup(request):
    error = ""

    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Check username already exists
            if User.objects.filter(username=username).exists():
                error = "exists"
            else:
                # Create Admin User
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )

                user.first_name = name
                user.save()

                error = "no"

        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()
            error = "yes"

    return render(request, "admin_signup.html", {"error": error})

def view_user(request):

    if not request.user.is_authenticated:
        return redirect('admin_login')

    data = StudentUser.objects.all()

    return render(
        request,
        'view_user.html',
        {'data': data}
    )   

def delete_user(request, user_id):

    if not request.user.is_authenticated:
        return redirect('admin_login')

    try:
        student = StudentUser.objects.get(
            id=user_id
        )

    except StudentUser.DoesNotExist:

        messages.error(
            request,
            "Student user not found."
        )

        return redirect('view_user')

    # Django User ko pehle save kar lo
    django_user = student.user

    # StudentUser delete
    student.delete()

    # Associated Django User delete
    if django_user:
        django_user.delete()

    messages.success(
        request,
        "Student user deleted successfully."
    )

    return redirect('view_user')

def change_status(request, user_id):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    user = Recruiter.objects.get(id=user_id)

    if user.status == "pending":
        user.status = "accepted"
    else:
        user.status = "rejected"

    user.save()

    return redirect('recruiter_pending')

def recruiter_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    data = Recruiter.objects.filter(status="pending")

    return render(
        request,
        'recruiter_pending.html',
        {'data': data}
    ) 
    
def change_status(request, recruiter_id):

    if not request.user.is_authenticated:
        return redirect('admin_login')

    recruiter = get_object_or_404(
        Recruiter,
        id=recruiter_id
    )

    if request.method == "POST":

        status = request.POST.get('status')

        recruiter.status = status
        recruiter.save()

        return redirect('recruiter_pending')

    return render(
        request,
        'change_status.html',
        {'recruiter': recruiter}
    ) 
    
def recruiter_accepted(request):

    if not request.user.is_authenticated:
        return redirect('admin_login')

    data = Recruiter.objects.filter(status='accepted')

    return render(
        request,
        'recruiter_accepted.html',
        {'data': data}
    )
    
def delete_recruiter(request, recruiter_id):

    if not request.user.is_authenticated:
        return redirect('admin_login')

    recruiter = get_object_or_404(
        Recruiter,
        id=recruiter_id
    )

    django_user = recruiter.user

    recruiter.delete()
    django_user.delete()

    return redirect('recruiter_accepted')

def recruiter_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    data = Recruiter.objects.filter(status='rejected')

    return render(
        request,
        'recruiter_rejected.html',
        {'data': data}
    ) 
    
def all_recruiters(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    data = Recruiter.objects.all()

    return render(
        request,
        'recruiter_all.html',
        {'data': data}
    )              
    
def change_passwordadmin(request):

    if not request.user.is_authenticated:
        return redirect('admin_login')

    if request.method == "POST":

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Old password check
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect.")
            return redirect('change_passwordadmin')

        # New password match
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('change_passwordadmin')

        # Password length
        if len(new_password) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters."
            )
            return redirect('change_passwordadmin')

        # Save new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        messages.success(
            request,
            "Password changed successfully."
        )

        return redirect('admin_home')

    return render(request, 'change_passwordadmin.html')    

def change_passworduser(request):

    if not request.user.is_authenticated:
        return redirect('user_login')

    if request.method == "POST":

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Old password check
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect!")
            return redirect('change_passworduser')

        # New password match
        if new_password != confirm_password:
            messages.error(
                request,
                "New password and confirm password do not match!"
            )
            return redirect('change_passworduser')

        # Password length
        if len(new_password) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters!"
            )
            return redirect('change_passworduser')

        # Save new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        messages.success(
            request,
            "Password changed successfully!"
        )

        return redirect('change_passworduser')

    return render(request, 'change_passworduser.html')

def change_passwordrecruiter(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    if request.method == "POST":

        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Old password check
        if not request.user.check_password(old_password):
            messages.error(request, "Old password is incorrect!")
            return redirect('change_passwordrecruiter')

        # New password match
        if new_password != confirm_password:
            messages.error(
                request,
                "New password and confirm password do not match!"
            )
            return redirect('change_passwordrecruiter')

        # Password length
        if len(new_password) < 8:
            messages.error(
                request,
                "Password must be at least 8 characters!"
            )
            return redirect('change_passwordrecruiter')

        # Save new password
        request.user.set_password(new_password)
        request.user.save()

        # Keep user logged in
        update_session_auth_hash(request, request.user)

        messages.success(
            request,
            "Password changed successfully!"
        )

        return redirect('change_passwordrecruiter')

    return render(request, 'change_passwordrecruiter.html')

def add_job(request):
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    error = ""

    if request.method == "POST":
        try:
            st = request.POST.get('start_date')
            ed = request.POST.get('end_date')
            t = request.POST.get('title')
            s = request.POST.get('salary')
            im = request.FILES.get('image')
            des = request.POST.get('description')
            exp = request.POST.get('experience')
            loc = request.POST.get('location')
            sk = request.POST.get('skills')
            cd = request.POST.get('creation_date')

            user = request.user

            # Get logged-in recruiter
            recruiter = Recruiter.objects.get(user=user)

            # Create Job
            Job.objects.create(
                recruiter=recruiter,
                start_date=st,
                end_date=ed,
                title=t,
                salary=s,
                image=im,
                description=des,
                experience=exp,
                location=loc,
                skills=sk,
                creation_date=cd
            )

            error = "no"

        except Recruiter.DoesNotExist:
            error = "recruiter_not_found"

        except Exception as e:
            print("ERROR:", e)
            traceback.print_exc()
            error = "yes"

    return render(request, "add_job.html", {"error": error})

def job_list(request):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    data = Job.objects.all()

    return render(request, 'job_list.html', {'data': data})
    
@require_POST
def delete_job(request, id):
    job = get_object_or_404(Job, id=id)
    job.delete()

    return redirect('job_list')   

def edit_jobdetail(request, id):

    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    job = get_object_or_404(Job, id=id)

    if request.method == "POST":

        print("========== UPDATE START ==========")
        print("Job ID:", job.id)
        print("POST DATA:", request.POST)

        # Get form data
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        title = request.POST.get('title')
        salary = request.POST.get('salary')
        description = request.POST.get('description')
        experience = request.POST.get('experience')
        location = request.POST.get('location')
        skills = request.POST.get('skills')
        creation_date = request.POST.get('creation_date')

        print("Start Date:", start_date)
        print("End Date:", end_date)
        print("Title:", title)
        print("Salary:", salary)
        print("Creation Date:", creation_date)

        # Update values
        job.start_date = datetime.strptime(
            start_date, "%Y-%m-%d"
        ).date()

        job.end_date = datetime.strptime(
            end_date, "%Y-%m-%d"
        ).date()

        job.title = title
        job.salary = salary
        job.description = description
        job.experience = experience
        job.location = location
        job.skills = skills

        if creation_date:
            job.creation_date = datetime.strptime(
                creation_date, "%Y-%m-%d"
            ).date()

        # Image
        if request.FILES.get('image'):
            job.image = request.FILES.get('image')

        # SAVE DATABASE
        job.save()

        print("UPDATED TITLE:", job.title)
        print("UPDATED SALARY:", job.salary)
        print("========== UPDATE SUCCESS ==========")

        return redirect(
            f"{reverse('edit_jobdetail', args=[job.id])}?updated=1"
        )

    return render(request, 'edit_jobdetail.html', {
        'job': job
    })
    
def latest_jobs(request):

    # Recruiter login check
    if not request.user.is_authenticated:
        return redirect('recruiter_login')

    # Get all jobs
    jobs = Job.objects.select_related(
        'recruiter'
    ).order_by('-id')

    return render(
        request,
        'latest_jobs.html',
        {
            'data': jobs
        }
    )  
def user_latestjobs(request):

    # Sabhi latest jobs
    jobs = Job.objects.select_related(
        'recruiter'
    ).order_by('-id')

    # Applied jobs ki ID
    applied_job_ids = []

    # Agar user login hai
    if request.user.is_authenticated:

        try:
            # Current logged-in user ka StudentUser
            student = StudentUser.objects.get(
                user=request.user
            )

            # Is student ne kin jobs par apply kiya hai
            applied_job_ids = list(
                Apply.objects.filter(
                    student=student
                ).values_list(
                    'job_id',
                    flat=True
                )
            )

        except StudentUser.DoesNotExist:
            applied_job_ids = []

    return render(
        request,
        'user_latestjobs.html',
        {
            'data': jobs,
            'applied_job_ids': applied_job_ids,
        }
    )
def user_latestjobs(request):

    # All jobs
    jobs = Job.objects.select_related(
        'recruiter'
    ).order_by('-id')

    # Applied job IDs
    applied_job_ids = []

    if request.user.is_authenticated:

        try:
            student = StudentUser.objects.get(
                user=request.user
            )

            applied_job_ids = list(
                Apply.objects.filter(
                    student=student
                ).values_list(
                    'job_id',
                    flat=True
                )
            )

        except StudentUser.DoesNotExist:
            applied_job_ids = []

    return render(
        request,
        'user_latestjobs.html',
        {
            'data': jobs,
            'applied_job_ids': applied_job_ids,
        }
    )
def applyforjob(request, id):

    if not request.user.is_authenticated:
        return redirect('user_login')

    job = get_object_or_404(Job, id=id)

    today = timezone.now().date()

    if job.end_date < today:

        messages.error(
            request,
            "This job application deadline has expired."
        )

        return redirect('user_latestjobs')

    try:

        student = StudentUser.objects.get(
            user=request.user
        )

    except StudentUser.DoesNotExist:

        messages.error(
            request,
            "Student profile not found."
        )

        return redirect('user_latestjobs')

    already_applied = Apply.objects.filter(
        job=job,
        student=student
    ).exists()

    return render(
        request,
        'applyforjob.html',
        {
            'job': job,
            'student': student,
            'already_applied': already_applied,
        }
    )
def upload_resume(request, id):

    if not request.user.is_authenticated:
        return redirect('user_login')

    job = get_object_or_404(Job, id=id)

    # Check job expiry
    today = timezone.now().date()

    if job.end_date < today:

        messages.error(
            request,
            "This job application deadline has expired."
        )

        return redirect('user_latestjobs')

    try:

        student = StudentUser.objects.get(
            user=request.user
        )

    except StudentUser.DoesNotExist:

        messages.error(
            request,
            "Student profile not found."
        )

        return redirect('user_latestjobs')

    # Check already applied
    already_applied = Apply.objects.filter(
        job=job,
        student=student
    ).exists()

    if already_applied:

        messages.warning(
            request,
            "You have already applied for this job."
        )

        return redirect('user_latestjobs')

    # Submit resume
    if request.method == "POST":

        resume = request.FILES.get('resume')

        if not resume:

            messages.error(
                request,
                "Please upload your resume."
            )

            return render(
                request,
                'upload_resume.html',
                {
                    'job': job
                }
            )

        Apply.objects.create(
            job=job,
            student=student,
            resume=resume,
            applydate=today
        )

        messages.success(
            request,
            "Job applied successfully!"
        )

        return redirect('user_latestjobs')

    return render(
        request,
        'upload_resume.html',
        {
            'job': job
        }
    )