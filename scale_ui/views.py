import time
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

# Import from existing app logic
from app.src.services.ai_service import AIService
from app.src.services.matching_service import MatchingService
from app.src.repositories.picklist_repository import PicklistRepository


def home(request):
    return render(request, 'home.html')


def classify(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']
        
        # Read image bytes
        try:
            image_bytes = uploaded_file.read()
        except Exception as e:
            return render(request, 'result.html', {'error': f"Error reading file: {e}"})

        # Initialize services
        # In a production app, we might load the repo once at startup/cache it
        picklist_repo = PicklistRepository()
        picklist_products = picklist_repo.load()
        
        ai_service = AIService()
        matching_service = MatchingService(picklist_products)

        # Call AI Service
        # Simple retry logic similar to main.py but limited
        agent_output = ""
        for _ in range(3):
            agent_output = ai_service.analyze_image(image_bytes)
            if "Error" in agent_output and "Exception" in agent_output:
                time.sleep(1)
                continue
            break
        
        if not agent_output or "Error" in agent_output:
             return render(request, 'result.html', {'error': "Could not identify item. Please try again."})

        # Match logic
        matches = matching_service.find_matches(agent_output)

        context = {}
        if len(matches) > 1:
            # Refine match
            refined_output_str = matching_service.refine_match(ai_service, matches)
            try:
                best_match_data = json.loads(refined_output_str)
                context['best_match'] = best_match_data
                context['found'] = True
            except json.JSONDecodeError:
                # Fallback if refinement returns invalid JSON
                context['best_match'] = matches[0].to_dict()
                context['found'] = True
            
        elif matches:
            context['best_match'] = matches[0].to_dict()
            context['found'] = True
        else:
            context['found'] = False
        
        return render(request, 'result.html', context)

    return redirect('home')
