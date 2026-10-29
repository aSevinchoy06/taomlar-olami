from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Ingredient, Recipe, RecipeIngredient


# ---------------------------------------------------------------------------
# Admin panel umumiy sozlamalari (sarlavhalar)
# ---------------------------------------------------------------------------
admin.site.site_header = "Taomlar — boshqaruv paneli"
admin.site.site_title = "Taomlar admin"
admin.site.index_title = "Boshqaruv paneliga xush kelibsiz"


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "recipe_count")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)

    @admin.display(description="Retseptlar soni")
    def recipe_count(self, obj):
        return obj.recipes.count()


# ---------------------------------------------------------------------------
# Ingredient
# ---------------------------------------------------------------------------
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "used_in_count")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="Nechta retseptda ishlatilgan")
    def used_in_count(self, obj):
        return obj.recipes.count()


# ---------------------------------------------------------------------------
# Recipe (ichiga RecipeIngredient inline qo'shilgan)
# ---------------------------------------------------------------------------
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    min_num = 1
    autocomplete_fields = ("ingredient",)
    verbose_name = "Ingredient"
    verbose_name_plural = "Tarkibiy qismlar (ingredientlar)"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "image_preview",
        "title",
        "category",
        "cooking_time_display",
        "servings",
        "created_at",
    )
    list_display_links = ("image_preview", "title")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "ingredients__name")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("category",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "large_image_preview")
    inlines = [RecipeIngredientInline]
    list_per_page = 25
    save_on_top = True

    fieldsets = (
        ("Asosiy ma'lumot", {
            "fields": ("title", "slug", "category", "description"),
        }),
        ("Rasm", {
            "fields": ("image", "large_image_preview"),
        }),
        ("Tayyorlash", {
            "fields": ("cooking_time", "servings", "instructions"),
        }),
        ("Qo'shimcha", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;'
                'object-fit:cover;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Rasm (katta)")
    def large_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:320px;max-height:320px;'
                'object-fit:cover;border-radius:10px;" />',
                obj.image.url,
            )
        return "Rasm yuklanmagan"

    @admin.display(description="Tayyorlash vaqti")
    def cooking_time_display(self, obj):
        return f"{obj.cooking_time} daqiqa"
