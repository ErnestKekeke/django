# decorators.py
from django.shortcuts import redirect

def checkage_required(view_func):
    """
    Decorator to ensure user is 18+ based on POSTed age or session.
    """
    def _wrapped_view(request, *args, **kwargs):
        # Try to get age from session
        age = request.session.get('age')

        # If age not in session and user submitted a POST form, store it
        if request.method == 'POST':
            try:
                posted_age = int(request.POST.get('age', 0))
                request.session['age'] = posted_age
                age = posted_age
            except ValueError:
                return redirect('calculator:home')  # invalid input

        # If age is missing or under 18, redirect to home
        if not age or age < 18:
            return redirect('calculator:home')

        # Otherwise, allow access
        return view_func(request, *args, **kwargs)

    return _wrapped_view