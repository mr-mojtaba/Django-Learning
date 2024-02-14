from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from .forms import *
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required



# Create your views here.
def index(request):
    return render(request, "blog/index.html")


# def post_list(request):
#     posts = Post.published.all()
#
#     # Creating an object of the paginator class.
#     paginator = Paginator(posts, 2)
#     # Specifying the page number.
#     page_number = request.GET.get('page', 1)
#     # Resetting the value with page_number.
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#
#     context = {
#         'posts': posts,
#     }
#     return render(request,"blog/list.html", context)

class PostListView(ListView):
    # Returns all posts.
    # model = Post

    # Returns published posts.
    queryset = Post.published.all()

    # Defining name for the object.
    context_object_name = "posts"

    paginate_by = 3
    template_name = "blog/list.html"


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    # Creating a variable and put the approved comments in it.
    comments = post.comments.filter(active=True)
    # Creating an empty form.
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, "blog/detail.html", context)

# class PostDetailView(DetailView):
#     model = Post
#     template_name = "blog/detail.html"


def ticket(request):
    if request.method == 'POST':
        # Creating a Variable from the TicketForm.
        form = TicketForm(request.POST)

        # Form data validation.
        if form.is_valid():
            # Creating an object from the Ticket model.
            ticket_obj = Ticket.objects.create()

            # Creating a variable and assigning it with form values.
            # (cleaned_data is a dictionary).
            cd = form.cleaned_data

            #  Initialization of each Ticket field with the values of each Ticket Form field.
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']

            # Storage in the database.
            ticket_obj.save()

            return redirect("blog:index")
    else:
        # Creating a variable from TicketForm with no value.
        form = TicketForm()

    # Show ticket.html page.
    return render(request, "forms/ticket.html", {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment,
    }
    return render(request, "forms/comment.html", context)


@login_required(login_url='/admin/login/')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form = PostForm
    else:
        form = PostForm()
    return render(request, 'forms/create_post.html', {'form': form})
