import os
from pyexpat import model
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from PIL import Image
from io import BytesIO
from typing import List, Optional, Text, Union
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

class RecipeOption(BaseModel):
    name: str
    description: Optional[str] = None

class RecipeSuggestions(BaseModel):
    recipes: List[RecipeOption]

class RecipeRequest(BaseModel):
    selected_recipe: str
    available_ingredients: Optional[List[str]] = None

class RecipeDetail(BaseModel):
    name: str
    ingredients: List[str]
    instructions: str
    missing_items: List[str]


@app.get("/")
def read_root():
    return {"message": "NutrieGenie is running successfully."}

@app.post("/suggestions/", response_model=RecipeSuggestions)
async def suggest_recipes(
    file: List[UploadFile] = File(default=[]),
    items: List[str] = Form(default=[])
):
    try:
        prompt = """
        Identify the ingredients from the user input and suggest 5 possible recipes with short descriptions.
        Return in pure JSON format as:
        {
            "recipes": [
                {"name": "Recipe Name", "description": "Short description"},
                ...
            ]
        }
        No markdown or code block formatting.
        """

        inputs = [prompt.strip()]
        if file:
            global detected_ingredient
            detected_ingredient = []
            for f in file:
                content = await f.read()
                image = Image.open(BytesIO(content))
                item_name = model.generate_content(["What food item is this image? Give only the name.", image]).text.strip()
                detected_ingredient.append(item_name)
            ingredients_text = ", ".join(detected_ingredient)
            inputs.append(f"Available ingredients: {ingredients_text}")
        elif items:
            global last_available_ingredients
            last_available_ingredients = items
            ingredients_text = ", ".join(items)
            inputs.append(f"Available ingredients: {ingredients_text}")
        else:
            raise HTTPException(status_code=400, detail="Provide either images or text ingredients.")
        
        response = model.generate_content(inputs)
        raw_text = response.text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text.lstrip("```json").rstrip("```").strip()

        suggestions = eval(raw_text) 
        return suggestions

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating suggestions: {str(e)}")

last_available_ingredients: List[str] = []
detected_ingredient: List[str] = []

@app.post("/recipe/", response_model=RecipeDetail)
async def get_full_recipe(request: RecipeRequest):
    
    try:
        global last_available_ingredients
        global detected_ingredient
        if not request.available_ingredients:
            if request.available_ingredients:
                pass
            elif last_available_ingredients:
                request.available_ingredients = last_available_ingredients
            elif detected_ingredient:
                request.available_ingredients = detected_ingredient
            else:
                request.available_ingredients = []

        ingredient_info = ", ".join(request.available_ingredients) if request.available_ingredients else "None"

        prompt = f"""
        You are a professional recipe assistant. The user has selected a recipe and also provided a list of available ingredients.

        Recipe Name: "{request.selected_recipe}"
        Available Ingredients: {ingredient_info} = {Form(default=[])}

        Your job is to return ONLY a JSON object in the exact format below, with **no markdown, no code blocks, and no explanation**.

        ### Important Rules (follow strictly):
        - Always give full recipe with step-by-step instructions (every time we exceute)
        - The `"ingredients"` list must include **only the full list of ingredients required** to make the selected recipe — do NOT filter based on what the user has.
        - The `"missing_items"` list must include **only those ingredients that are in the 'ingredients' list but NOT in the user's available ingredients**.
        - Do NOT include all ingredients again in the `"missing_items"` — include only the ones that the user doesn't already have.
        - Use concise but complete values — no comments, no markdown.

        ### Output Format:
        {{
        "name": "Recipe Name",
        "ingredients": ["required ingredient 1", "required ingredient 2", "..."],
        "instructions": "Step-by-step instructions to prepare the dish.",
        "missing_items": ["ingredient not found in available ingredients list", "..."]
        }}
        """

        response = model.generate_content(prompt.strip())
        raw_text = response.text.strip()

        if raw_text.startswith("```json"):
            raw_text = raw_text.lstrip("```json").rstrip("```").strip()

        recipe_data = eval(raw_text) 
        return recipe_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")