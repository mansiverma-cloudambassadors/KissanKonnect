import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from PIL import Image
from io import BytesIO
from typing import List, Optional
from pydantic import BaseModel
import google.generativeai as genai


app = FastAPI()

genai.configure(api_key=os.getenv("API_KEY"))

class Ingredient(BaseModel):
    name: str
    calories: Optional[str]
    carbs: Optional[str]
    protein: Optional[str]
    fat: Optional[str]

class NutritionSummary(BaseModel):
    calories: Optional[str]
    protein: Optional[str]
    carbs: Optional[str]
    fat: Optional[str]
    sodium: Optional[str]

class AnalysisResponse(BaseModel):
    ingredients: List[Ingredient]
    total_nutrition_estimate: NutritionSummary

@app.get("/")
def read_root():
    return {"message": "NutrieGenie is running successfully."}

@app.post("/analyze/")
async def analyze_item(
    file: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)  
):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        if file:
            content = await file.read()
            image = Image.open(BytesIO(content))
            prompt = """
            Identify ingredients and their nutritional values in this image in detailed version with explanation.
            Respond ONLY with a valid JSON in this format (no markdown):

            {
              "ingredients": [
                {
                  "name": "Ingredient name",
                  "calories": "X",
                  "carbs": "Y",
                  "protein": "Z",
                  "fat": "W"
                }
              ],
              "total_nutrition_estimate": {
                "calories": "X",
                "protein": "Y",
                "carbs": "Z",
                "fat": "W",
                "sodium": "U"
              }
            }
            """
            response = model.generate_content([prompt.strip(), image])

        elif text:
            prompt = f"""
            Analyze the following ingredients or recipe and provide nutritional details in detailed version with explanation.
            Respond ONLY with a valid JSON in this format (no markdown):

            {{
              "ingredients": [...],
              "total_nutrition_estimate": {{
                "calories": "X",
                "protein": "Y",
                "carbs": "Z",
                "fat": "W",
                "sodium": "U"
              }}
            }}

            Recipe/Ingredients: {text}
            """
            response = model.generate_content(prompt.strip())
            
        else:
            raise HTTPException(status_code=400, detail="Please provide either an image or text.")

        return {"ingredients_analysis": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))