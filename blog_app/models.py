from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

# --------category model ------#
class Category(models.Model):
    cat_title = models.CharField(
        max_length=255,
        verbose_name='Category Title',
        help_text="create unique title for the Category 'Max Length: 255'",
        unique=True,
        null=True,
        blank=False)

    cat_des = models.CharField(
        max_length=255,
        verbose_name='Category Description',
        help_text=" create short descirption about this Category 'Max Length: 255'",
        unique=False,
        null=True,
        blank=False)

    cat_created = models.DateTimeField(
        verbose_name='Category Created Date',
        auto_now_add=True,
        auto_now=False,
        null=True)

    cat_updated = models.DateTimeField(
        verbose_name='Category Updated Date',
        auto_now_add=False,
        auto_now=True,
        null=True)

    cat_image = models.ImageField(
        verbose_name='Category Image',
        help_text=' create Category Image',
        upload_to='cats_images/%Y/%m/%d/',
        default='default.jpg',
        null = True)

    class Meta:
        ordering = ('-cat_created',)
    
    

    #  counter of posts belong to this category 
    def posts_for_cat_count(self):
        return Post.objects.all().filter(cat_fk=self.id).count()


    def __str__(self):
        return self.cat_title


    # def get_absolute_url(self):
    #     return reverse('blog_app:cat_detail', args=[str(self.id)])




# ------ Post model ---------------------#
class Post(models.Model):
    cat_fk = models.ForeignKey(
        Category,
        verbose_name='Category FK',
        on_delete=models.CASCADE,
        related_name='posts_to_cat')
    
    # must name be --- user_fk
    post_author = models.ForeignKey(
        User,
        verbose_name='Post author',
        on_delete=models.CASCADE,
        related_name='posts_to_author')

   
    post_title = models.CharField(
        verbose_name='Post subject',
        max_length=255,
        unique=True,
        help_text="create unique subject of your post 'Max Length: 255'",
        blank=False,
        null=True)
    
    post_text = models.TextField(
        verbose_name='Post text',
        max_length=4000,
        unique=False,
        help_text="createyour post 'Max Length: 4000'",
        blank=False,
        null=True)

    
    post_created = models.DateTimeField(
        verbose_name='Post Created Date',
        auto_now_add=True,
        auto_now=False,
        null=True)

    post_updated = models.DateTimeField(
        verbose_name='Post Updated Date',
        auto_now_add=False,
        auto_now=True,
        null=True)

    post_views_counter = models.PositiveIntegerField(default=0)
    
    
    # post_like = models.ManyToManyField(
    #     User,
    #     blank=True)

   

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    post_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published')


    class Meta:
      ordering = ('-post_created',)
    
    def __str__(self):
        return self.post_title


    #  get number of comments belong to each post
    def comments_for_post_count(self):
        return Comment.objects.all().filter(post_fk=self.id).count()
    



    # get author name belong each post: --- not good to use__ not need :(
    # def author_for_each_post(self):
    #     return User.objects.all().filter(username=self.post_author)


    def get_absolute_url(self):
      return reverse('blog_app:post_detail', args=[str(self.id)])








# ------------------Comment model ----------#
class Comment(models.Model):
    post_fk = models.ForeignKey(
        Post,
        verbose_name='Post FK',
        on_delete=models.CASCADE,
        related_name='comments_to_post')

    comment_author = models.ForeignKey(
        User,
        verbose_name='Comment author',
        on_delete=models.CASCADE,
        related_name='Comments_to_author')


    comment_text = models.TextField(
        verbose_name='Comment text',
        max_length=4000,
        unique=False,
        help_text="create your Comment 'Max Length: 4000'",
        blank=False,
        null=True)


    comment_created = models.DateTimeField(
        verbose_name='Comment Created Date',
        auto_now_add=True,
        auto_now=False,
        null=True)


    comment_updated = models.DateTimeField(
        verbose_name='Comment Updated Date',
        auto_now_add=False,
        auto_now=True,
        null=True)


    # comments_views_counter = models.PositiveIntegerField(default=0)


    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    comment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published')

    class Meta:
      ordering = ('-comment_created',)

    def __str__(self):
        return self.comment_text





    # comment_like = models.ManyToManyField( -- not work !!
        #     User,
        #     blank=True)



    

    #  add a new comment counter belong to this post
    # def add_comment_counter(self):
    #     number_of_comments=Comment.objects.all().count()
    #     add_comment_count = number_of_comments+1
    #     return add_comment_count
