# middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class CheckAgeMiddleware:
    """
    Middleware to check age from a POST form before accessing the protected page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check for the specific protected page
        protected_path = reverse('blog:agepage')

        if request.path == protected_path:
            age = request.POST.get('age')
            if age:
                try:
                    age = int(age)
                    if age < 18:
                        # Redirect back to the form if under 18
                        # return redirect('age_form')
                        return redirect('blog:index')
                except ValueError:
                    # Invalid input, redirect back to form
                    # return redirect('age_form')
                    return redirect('blog:index')
            else:
                # No age submitted, redirect to form
                # return redirect('age_form')
                return redirect('blog:index')

        response = self.get_response(request)
        return response