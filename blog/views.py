from notification.models import Notification
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Comment, Post
from .forms import CommentForm
from django.http import HttpResponseRedirect, JsonResponse
from users.models import Profile
from itertools import chain
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
import random
from .forms import CommentReportForm
from .models import CommentReport
from blog.models import Post
from blog.utils import is_ajax
from .models import Post, Tag
from django.db.models import Q
from django.views.decorators.http import require_POST




""" Home page with all posts """
def first(request):
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'blog/first.html', context)

""" Posts of following user profiles """
@login_required
def posts_of_following_profiles(request):

    profile = Profile.objects.get(user = request.user)
    users = [user for user in profile.following.all()]
    posts = []
    qs = None
    for u in users:
        p = Profile.objects.get(user=u)
        p_posts = p.user.post_set.all()
        posts.append(p_posts)
    my_posts = profile.profile_posts()
    posts.append(my_posts)
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj:obj.date_posted)

    paginator = Paginator(qs, 5)
    page = request.GET.get('page')
    try:
        posts_list = paginator.page(page)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)
  
    return render(request,'blog/feeds.html',{'profile':profile,'posts':posts_list})


@login_required
@require_POST
def LikeView(request):
    post_id = request.POST.get('id') or request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
        # Remove notification
        Notification.objects.filter(
            post=post, 
            sender=request.user, 
            notification_type=1
        ).delete()
    else:
        post.likes.add(request.user)
        liked = True
        # Create notification
        Notification.objects.create(
            post=post, 
            sender=request.user, 
            user=post.author, 
            notification_type=1
        )
        liked = request.user.is_authenticated and post.likes.filter(id=request.user.id).exists()
    context = {
        'post': post,
        'total_likes': post.total_likes(),
        'liked': liked,
    }
    
    # Check for AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('blog/like_section.html', context, request=request)
        return JsonResponse({'form': html})
    
    return redirect('post-detail', pk=post.pk)


""" Post save """
@login_required
def SaveView(request):

    post = get_object_or_404(Post, id=request.POST.get('id'))
    saved = False
    if post.saves.filter(id=request.user.id).exists():
        post.saves.remove(request.user)
        saved = False
    else:
        post.saves.add(request.user)
        saved = True
    
    context = {
        'post':post,
        'total_saves':post.total_saves(),
        'saved':saved,
    }

    if is_ajax(request=request):
        html = render_to_string('blog/save_section.html',context, request=request)
        return JsonResponse({'form':html})


""" Like post comments """
@login_required
def LikeCommentView(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    comment_id = request.POST.get('comment_id')
    if not comment_id:
        return JsonResponse({'error': 'Comment ID is required'}, status=400)

    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post  # Assuming you have a post field in your Comment model

    # Toggle like
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    # Prepare context for AJAX response
    total_comments = post.comments.filter(reply=None).order_by('-id')

    # Create likes dictionary
    tcl = {}
    for cmt in post.comments.all():
        tcl[cmt.id] = cmt.likes.filter(id=request.user.id).exists()

    context = {
        'post': post,
        'comments': total_comments,
        'clikes': tcl,
        'user': request.user
    }

    # Check if request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('blog/comments.html', context, request=request)
        return JsonResponse({
            'form': html,
            'total_likes': comment.total_clikes(),
            'is_liked': comment.likes.filter(id=request.user.id).exists()
        })

    return redirect('post-detail', pk=post.id)



""" Home page with all posts """
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' 
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, *args,**kwargs):
        context = super(PostListView, self).get_context_data()
        users = list(User.objects.exclude(pk=self.request.user.pk))
        if len(users) > 3:
            cnt = 3
        else:
            cnt = len(users)
        random_users = random.sample(users, cnt)
        context['random_users'] = random_users
        return context


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm
from notification.models import Notification
from django.contrib.auth.models import User

# All the posts of the user
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# Post detail view with comment handling and media support
@login_required
def PostDetailView(request, pk):
    stuff = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        # Pass both POST data and FILES to the form
        comment_form = CommentForm(request.POST, request.FILES)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.name = request.user
            comment.post = stuff

            # Handle media files (image, video, voice)
            if 'image' in request.FILES:
                comment.image = request.FILES['image']
            if 'video' in request.FILES:
                comment.video = request.FILES['video']
            if 'voice' in request.FILES:
                comment.voice = request.FILES['voice']

            # Handle reply if exists
            reply_id = request.POST.get('comment_id')
            if reply_id:
                comment.reply = Comment.objects.get(id=reply_id)
                # Notification for reply
                notify = Notification(
                    post=stuff,
                    sender=request.user,
                    user=stuff.author,
                    text_preview=comment.body,
                    notification_type=4
                )
            else:
                # Notification for new comment
                notify = Notification(
                    post=stuff,
                    sender=request.user,
                    user=stuff.author,
                    text_preview=comment.body,
                    notification_type=3
                )

            comment.save()
            notify.save()

            # Handle AJAX requests for comments
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                total_comments = stuff.comments.filter(reply=None).order_by('-id')
                total_comments2 = stuff.comments.all().order_by('-id')
                
                tcl = {}
                for cmt in total_comments2:
                    tcl[cmt.id] = cmt.likes.filter(id=request.user.id).exists()
                
                context = {
                    'post': stuff,
                    'comments': total_comments,
                    'clikes': tcl,
                }
                
                html = render_to_string('blog/comments.html', context, request=request)
                return JsonResponse({'form': html})
                
    else:
        comment_form = CommentForm()

    # Get all comments and replies for the post
    total_comments = stuff.comments.filter(reply=None).order_by('-id')
    total_comments2 = stuff.comments.all().order_by('-id')

    # Create likes dictionary
    tcl = {}
    for cmt in total_comments2:
        tcl[cmt.id] = cmt.likes.filter(id=request.user.id).exists()

    context = {
        'post': stuff,
        'comments': total_comments,
        'comment_form': comment_form,
        'clikes': tcl,
    }

    return render(request, 'blog/post_detail.html', context)


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Post, PostImage, PostDocument, PostVideo
from .forms import PostForm
from django.urls import reverse_lazy


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        
        return response


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
       
        return response

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

""" About page """
def about(request):
    return render(request, 'blog/about.html', {'title':'About'})
from django.shortcuts import render
from .models import Post, Tag  # Add Tag to the imports

from django.shortcuts import render
from django.db.models import Q
from .models import Post, Tag


'''search'''
def search(request):
    query = request.GET.get('query', '').strip()
    tag_query = request.GET.get('tag', '')

    # Initialize with no results for invalid queries
    if not query or len(query) >= 150:
        allposts = Post.objects.none()
    else:
        # Use Q objects to combine searches
        allposts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()  # distinct() works here because we're not using union()

    # Additional tag filter if specified
    if tag_query:
        allposts = allposts.filter(tags__name=tag_query)

    # Get all available tags for the filter dropdown
    all_tags = Tag.objects.all().order_by('name')

    params = {
        'allposts': allposts,
        'query': query,
        'tag_query': tag_query,
        'all_tags': all_tags,
        'no_results': not allposts.exists(),
        'total_results': allposts.count()
    }
    
    return render(request, 'blog/search_results.html', params)

""" Liked posts """
@login_required
def AllLikeView(request):
    user = request.user
    liked_posts = user.blogpost.all()
    context = {
        'liked_posts':liked_posts
    }
    return render(request, 'blog/liked_posts.html', context)


""" Saved posts """
@login_required
def AllSaveView(request):
    user = request.user
    saved_posts = user.blogsave.all()
    context = {
        'saved_posts':saved_posts
    }
    return render(request, 'blog/saved_posts.html', context)


@login_required
def comment_edit(request, pk):  # Changed from comment_id to pk
    comment = get_object_or_404(Comment, id=pk)  # Changed to use pk
    
    # Check if user is the comment owner
    if comment.name != request.user:
        messages.error(request, "You cannot edit this comment.")
        return redirect('post-detail', pk=comment.post.id)
    
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            # Handle media files
            if 'image' in request.FILES:
                # Delete old image if exists
                if comment.image:
                    comment.image.delete()
                comment.image = request.FILES['image']
            elif 'image-clear' in request.POST:
                comment.image.delete()
                comment.image = None

            if 'video' in request.FILES:
                if comment.video:
                    comment.video.delete()
                comment.video = request.FILES['video']
            elif 'video-clear' in request.POST:
                comment.video.delete()
                comment.video = None

            if 'voice' in request.FILES:
                if comment.voice:
                    comment.voice.delete()
                comment.voice = request.FILES['voice']
            elif 'voice-clear' in request.POST:
                comment.voice.delete()
                comment.voice = None

            form.save()
            messages.success(request, "Comment updated successfully!")
            return redirect('post-detail', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'post': comment.post
    }
    
    return render(request, 'blog/comment_edit.html', context)

@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    
    # Check if user is the comment owner or admin
    if comment.name != request.user and not request.user.is_staff:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': "You cannot delete this comment."
            }, status=403)
        messages.error(request, "You cannot delete this comment.")
        return redirect('post-detail', pk=comment.post.id)
    
    if request.method == "POST":
        try:
            post_id = comment.post.id
            
            # Delete associated media files
            if comment.image:
                comment.image.delete()
            if comment.video:
                comment.video.delete()
            if comment.voice:
                comment.voice.delete()
                
            comment.delete()
            
            # Handle AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'message': 'Comment deleted successfully',
                    'comment_id': pk  # Send back the comment ID
                })
            
            messages.success(request, "Comment deleted successfully!")
            return redirect('post-detail', pk=post_id)
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                }, status=500)
            messages.error(request, f"Error deleting comment: {str(e)}")
            return redirect('post-detail', pk=comment.post.id)
    
    # For GET requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid request method'
        }, status=400)
        
    context = {
        'comment': comment,
        'post': comment.post
    }
    
    return render(request, 'blog/comment_confirm_delete.html', context)
@login_required
def report_comment(request, pk):  # Changed from comment_id to pk
    comment = get_object_or_404(Comment, id=pk)  # Changed to use pk
    
    # Prevent self-reporting
    if comment.name == request.user:
        messages.error(request, "You cannot report your own comment.")
        return redirect('post-detail', pk=comment.post.id)
    
    # Check if user has already reported this comment
    if comment.reported_by.filter(id=request.user.id).exists():
        messages.warning(request, "You have already reported this comment.")
        return redirect('post-detail', pk=comment.post.id)
    
    if request.method == "POST":
        reason = request.POST.get('reason')
        details = request.POST.get('details', '')
        
        report = CommentReport.objects.create(
            comment=comment,
            reported_by=request.user,
            reason=reason,
            details=details
        )
        
        comment.reported_by.add(request.user)
        
        # If comment gets more than 5 reports, hide it
        if comment.reported_by.count() >= 5:
            comment.is_hidden = True
            comment.save()
            
        messages.success(request, "Comment reported successfully.")
        return redirect('post-detail', pk=comment.post.id)
    
    context = {
        'comment': comment,
        'form': CommentReportForm()
    }
    
    return render(request, 'blog/report_comment.html', context)

from django.utils import timezone
from datetime import timedelta
from .models import UserContribution

from django.utils import timezone

from django.utils import timezone
from datetime import timedelta

def first_page(request):
    top_contributors = UserContribution.objects.order_by('-contribution_score')[:5]
    context = {
        'top_contributors': top_contributors
    }
    return render(request, 'blog/first.html', context)

def contributors_view(request):
    top_contributors = UserContribution.objects.order_by('-contribution_score')[:5]
    return render(request, 'blog/contributors.html', {
        'top_contributors': top_contributors
    })