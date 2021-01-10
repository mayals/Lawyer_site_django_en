from .models import Comment,Post
from django import forms



# ----- add post form --------#
class PostForm(forms.ModelForm):
    post_title = forms.CharField(label='Post Title', max_length=100,required=True, disabled=False)
    post_text = forms.CharField(label='Post Text',
                                max_length=4000,
                                help_text='the max length of this field is 4000',
                                widget = forms.Textarea(attrs={'rows': 5, 'placeholder': 'put your opinion in this post here .. '}))
    class Meta:
        model = Post
        fields = ('post_title', 'post_text')




# ----- add comment form --------#
class CommentForm(forms.ModelForm):
    comment_text = forms.CharField(label='Comment Text',
                                max_length=4000,
                                help_text='the max length of this field is 4000',
                                widget=forms.Textarea(
                                    attrs={'rows': 5, 'placeholder': 'comment here .. '}))
    class Meta:
        model = Comment
        fields = ['comment_text']
