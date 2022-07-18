from django import forms
from stocks. models import products
from category. models import category

class add_product(forms.ModelForm):
    class Meta:
        model=products
        fields=['product_name','description','max_area','bedrooms','bathrooms','floors','parking','price','images','category']
        def __init__(self,*args,**kwargs) :
            super(add_product,self).__init__(*args,**kwargs)
            self.fields['product_name'].widget.attrs['placeholder'] = 'Enter product Name'
            self.fields['description'].widget.attrs['placeholder'] = 'description'
            self.fields['max_area'].widget.attrs['placeholder'] = 'max_area'
            self.fields['bedrooms'].widget.attrs['placeholder'] = 'bedrooms'
            self.fields['bathrooms'].widget.attrs['placeholder'] = 'bathrooms'
            self.fields['floors'].widget.attrs['placeholder'] = 'floors'
            self.fields['parking'].widget.attrs['placeholder'] = 'parking'
            self.fields['price'].widget.attrs['placeholder'] = 'price'
            self.fields['category'].widget.attrs['placeholder'] = 'category'

            for field in self.fields:
                
                self.fields[field].widget.attrs['class']='form-control'
            
class edit_product(forms.ModelForm):
    class Meta:
        model=products
        fields=['product_name','description','max_area','bedrooms','bathrooms','floors','parking','price','images','category']
        
    def __init__(self,*args,**kwargs):
        super(edit_product,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            # self.fields['is_available'].widget.attrs['class'] =''  