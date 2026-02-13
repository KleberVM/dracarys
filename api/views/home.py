from django.shortcuts import render

def home_dracarys(request):
    """Renderiza la página de inicio usando el sistema de templates."""
    # Django buscará dentro de api/templates/api/index.html
    return render(request, 'index.html')