from wsgiref.validate import validator

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Poll, Question, Choice


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError("%(value)s ไม่ใช้เลขคู่", params={"value":value})

class PollForm(forms.Form):
    title = forms.CharField(label='ชื่อโพล', max_length=100,required=True)
    email = forms.CharField(validators=[validate_email], required=False)
    no_question = forms.IntegerField(label='จำนวนคำถาม',min_value=0,max_value=10,required=True, validators=[validate_even])
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)

    def clean_title(self):
        data = self.cleaned_data['title']
        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        clean = super().clean()
        start = clean.get('start_date')
        end = clean.get('end_date')
        if(start and not end):
            raise forms.ValidationError("โปรดเลือกวันสิ้นสุด")
        elif(end and not start):
            raise forms.ValidationError("โปรดเลือกวันเริ่มต้น")

class PollModelForm(forms.ModelForm):
    # email = forms.CharField(validators=[validate_email], required=False)
    # no_question = forms.IntegerField(label='จำนวนคำถาม', min_value=0, max_value=10, required=True,
    #                                  validators=[validate_even])
    class Meta:
        model = Poll
        exclude = ['del_flag']

    def clean_title(self):
        data = self.cleaned_data['title']
        if "ไอทีหมีแพนด้า" not in data:
            raise forms.ValidationError("คุณลืมชื่อคณะ")
        return data

    def clean(self):
        clean = super().clean()
        start = clean.get('start_date')
        end = clean.get('end_date')
        if(start and not end):
            raise forms.ValidationError("โปรดเลือกวันสิ้นสุด")
        elif(end and not start):
            raise forms.ValidationError("โปรดเลือกวันเริ่มต้น")

class QuestionForm(forms.Form):
    question_id = forms.IntegerField(required=False, widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea)
    type = forms.ChoiceField(choices=Question.TYPES, initial='01')

class ChoiceModelForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = "__all__"

class CommentForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    body = forms.CharField(max_length=500)
    email = forms.CharField(required=False)
    tel = forms.CharField(max_length=10, required=False)
    def clean_email(self):
        value = self.cleaned_data['email']
        if(value):
            try:
                validate_email(value)
            except ValidationError as e:
                raise forms.ValidationError("Enter a valid email address")
        return value


    def clean_tel(self):
        value = self.cleaned_data['tel']
        if(value):
            if (len(value) > 10 or len(value) < 10):
                raise forms.ValidationError("หมายเลขโทรศัพท์ต้องมี 10 หลัก")
            elif (len(value) < 10 and not value.isdigit()):
                self.add_error('tel', "หมายเลขโทรศัพท์ต้องมี 10 หลัก")
                self.add_error('tel', "หมายเลขโทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
            elif (not value.isdigit()):
                raise forms.ValidationError("หมายเลขโทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        return value


    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        tel = clean_data.get('tel')

        if(not email and not tel):
            raise forms.ValidationError("ต้องกรอก email หรือ phone number")


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label="รหัสผ่านเก่า")
    new_password1 = forms.CharField(label="รหัสผ่านใหม่")
    new_password2 = forms.CharField(label="ยืนยันรหัสผ่าน")

    def clean_newpassword1(self):
        value = self.cleaned_data['new_password1']

        if(len(value) < 8):
            raise forms.ValidationError("รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
        return value
    def clean_newpassword2(self):
        value = self.cleaned_data['new_password2']

        if(len(value) < 8):
            raise forms.ValidationError("รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
        return value

    def clean(self):
        clean = super().clean()
        pass1 = clean.get('new_password1')
        pass2 = clean.get('new_password2')

        if(pass1 != pass2):
            raise forms.ValidationError("รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านต้องเหมือนกัน")
        elif(pass1==pass2):
            if(len(pass1) < 8 and len(pass2) < 8):
                self.add_error('new_password1', "รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
                self.add_error('new_password2', "รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

class RegisterForm(forms.Form):
    email = forms.CharField(label="email", validators=[validate_email])
    username = forms.CharField(label="username", required=True)
    password1 = forms.CharField(label="password", widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label="re-password", widget=forms.PasswordInput, required=True)
    line_id = forms.CharField(label="line id", max_length=100, required=False)
    facebook = forms.CharField(label="facebook", max_length=100, required=False)
    MALE = "M"
    FEMALE = "F"
    OTHER = "X"
    GENDERS = (
        (MALE, 'ชาย'),
        (FEMALE, 'หญิง'),
        (OTHER, 'อื่น'),
    )
    gender = forms.ChoiceField(label="gender", widget=forms.RadioSelect(), required=True, choices=GENDERS)
    birthday = forms.DateField(label="birthday", required=False)


    def clean(self):
        clean = super().clean()
        pass1 = clean.get('password1')
        pass2 = clean.get('password2')
        if(pass1 != pass2):
            raise forms.ValidationError("รหัสผ่านใหม่ กับ ยืนยันรหัสผ่านต้องเหมือนกัน")
        elif(pass1==pass2):
            if(len(pass1) < 8 and len(pass2) < 8):
                self.add_error('password1', "รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")
                self.add_error('password2', "รหัสผ่านใหม่ต้องมีตัวอักษรมากกว่า 8 ตัวอักษร")

    # class Meta:
    #     model = User
    #     fields = ['username', 'email', 'password1', 'password2']
