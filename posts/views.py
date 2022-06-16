from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from posts.forms import PostCreationForm, PostUpdateForm,CreateCommentfrom
from posts.models import Post,category,tag


class index_wiev(ListView):
    template_name = 'posts/index.html'
    model=Post
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(index_wiev,self).get_context_data(**kwargs)
        context['slider_posts']=Post.objects.all().filter(slider_posts=True)
        return context


class PostDetailView(DetailView,FormMixin):
    template_name = 'posts/detail.html'
    model =Post
    context_object_name = 'single'
    form_class = CreateCommentfrom

    def get(self, request, *args, **kwargs):
        self.hit=Post.objects.filter(id=self.kwargs['pk']).update(hit=F('hit')+1)
        return super(PostDetailView,self).get(request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['previous']=Post.objects.filter(id__lt=self.kwargs['pk']).order_by('-pk').first()
        context['next']=Post.objects.filter(id__gt=self.kwargs['pk']).order_by('pk').first()
        context['form']=self.get_form()
        return context
    def form_valid(self, form):
        if form.is_valid():
            form.instance.post=self.object
            form.save()
            return super(PostDetailView, self).form_valid(form)
        else:
            return super(PostDetailView, self).form_invalid(form)

    def post(self,*args,**kwargs):
        self.object=self.get_object()
        form=self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_valid(form)

    def get_success_url(self):
        return reverse('detail',kwargs={'pk':self.object.pk,"slug":self.object.slug})




class CategoryDetail(ListView):
    model =Post
    template_name ='categories/category_detail.html'
    context_object_name ='posts'
    paginate_by = 3

    def get_queryset(self):
        self.category1=get_object_or_404(category,pk=self.kwargs['pk'])
        return Post.objects.filter(category=self.category1).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoryDetail, self).get_context_data(**kwargs)
        self.category1=get_object_or_404(category,pk=self.kwargs['pk'])
        context['category']=self.category1
        return context

class TagDetail(ListView):
    model=Post
    template_name = "tags/tag_detail.html"
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        self.tag1=get_object_or_404(tag,slug=self.kwargs['slug'])
        return Post.objects.filter(tag=self.tag1).order_by('id')

    def get_context_data(self,**kwargs):
        context=super(TagDetail,self).get_context_data(**kwargs)
        self.tag1=get_object_or_404(tag,slug=self.kwargs['slug'])
        context['tag']=self.tag1
        return context

@method_decorator(login_required(login_url='/users/login'),name="dispatch")
class PostCreateView(SuccessMessageMixin,CreateView):
    template_name = 'posts/create-post.html'
    form_class = PostCreationForm
    model=Post
    success_message = "yazı eklendi"
    #success_url = 'detail/<int:pk>/<slug:slug>'

    def get_success_url(self):
        return reverse('detail',kwargs={"pk":self.object.pk,"slug":self.object.slug})


    def form_valid(self, form):
        form.instance.user=self.request.user
        form.save()
        tags=self.request.POST.get('tag').split(',')

        for Tag1 in tags:
            current_tag=tag.objects.filter(slug=slugify(Tag1))

            if current_tag.count()<1:
                create_tag=tag.objects.create(title=Tag1)
                form.instance.tag.add(create_tag)
            else:
                exist_tag=tag.objects.get(slug=slugify(Tag1))
                form.instance.tag.add(exist_tag)

        return super(PostCreateView,self).form_valid(form)

@method_decorator(login_required(login_url='/users/login'),name="dispatch")
class UpdatePostView(UpdateView):
    model=Post
    template_name='posts/post-update.html'
    form_class = PostUpdateForm

    def get_success_url(self):
        return reverse('detail',kwargs={"pk":self.object.pk,"slug":self.object.slug})


    def form_valid(self, form):
        form.instance.user=self.request.user
        form.instance.tag.clear()

        tags=self.request.POST.get('tag').split(',')

        for Tag1 in tags:
            current_tag=tag.objects.filter(slug=slugify(Tag1))

            if current_tag.count()<1:
                create_tag=tag.objects.create(title=Tag1)
                form.instance.tag.add(create_tag)
            else:
                exist_tag=tag.objects.get(slug=slugify(Tag1))
                form.instance.tag.add(exist_tag)
        return super(UpdatePostView,self).form_valid(form)
#########Her kullanıcının kendi postunu düzenleme yapmasına olanak sağlayan koddur#########
    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect('/')
        return super(UpdatePostView,self).get(request,*args,**kwargs)


@method_decorator(login_required(login_url='/users/login'),name='dispatch')
class DeletePostView(DeleteView):
    model = Post
    success_url = "/"
    template_name = "posts/delete.html"

    def delete(self, request, *args, **kwargs):
        self.object=self.get_object()
        if self.object.user==request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)


    def get(self, request, *args, **kwargs):
        self.object=self.get_object()

        if self.object.user != request.user:
            return HttpResponseRedirect("/")

        return super(DeletePostView,self).get(request,*args,**kwargs)
class SearhView(ListView):
    model=Post
    template_name = "posts/search.html"
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        query=self.request.GET.get("q")

        if query:
            return Post.objects.filter(Q(title__icontains=query) |
                                       Q(content__icontains=query) |
                                       Q(tag__title__icontains=query)
                                      ).order_by('id').distinct()
        return Post.objects.all().order_by('id')














