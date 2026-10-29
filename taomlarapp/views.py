
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Recipe, Category


def home(request):
    recipes = Recipe.objects.select_related("category").all()
    categories = Category.objects.all()

    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()

    if query:
        recipes = recipes.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(ingredients__name__icontains=query)
        ).distinct()

    if category_slug:
        recipes = recipes.filter(category__slug=category_slug)

    context = {
        "recipes": recipes,
        "categories": categories,
        "query": query,
        "selected_category": category_slug,
    }

    return render(request, "taomlarapp/home.html", context)


def recipe_detail(request, slug):
    recipe = get_object_or_404(
        Recipe.objects.select_related("category").prefetch_related(
            "ingredients",
            "recipeingredient_set__ingredient",
        ),
        slug=slug,
    )

    return render(
        request,
        "taomlarapp/detail.html",
        {"recipe": recipe},
    )
