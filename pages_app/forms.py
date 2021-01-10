from django import forms


class ContactUsForm(forms.Form):
    subject = forms.CharField(
        label='Subject',
        max_length=100,
        required=True,
        disabled=False)


    from_email = forms.EmailField(
        max_length=200,
        label='sender Email',
        required=True)


    message = forms.CharField(
        label='Text',
        required=True,
        max_length=4000,
        help_text='the max length of text field is 4000',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'put your Request here ..'}))






    # this field not work
    # full_name = forms.CharField(
    #     max_length= 100,
    #     label=' sender Full Name',
    #     required=True)



    # this field not work
    # Mobile_num = forms.CharField(
    #     initial='00966*********',
    #     max_length=14,
    #     label='sender Mobile(WhatsApp) Number',
    #    required=True)


    
    
   
    
