#!/usr/bin/env python3
"""
Multimodal Image Processing using TensorZero Gateway
"""

import os
import base64
import mimetypes
from pathlib import Path
from tensorzero import TensorZeroGateway

class MultimodalImageProcessor:
    def __init__(self):
        # No need for separate uploads directory - we'll work directly with sources
        pass
    
    def process_image(self, image_path):
        """
        Process an image using multimodal inference
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Analysis result with description and metadata
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            return {
                "status": "error",
                "error": f"Image file not found: {image_path}",
                "content": f"[Image not found: {image_path}]"
            }
        
        # Processing image with multimodal AI
        
        try:
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(image_path))
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/jpeg'  # Default fallback
            
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Image processed for multimodal analysis
            
            # Use TensorZero Gateway for multimodal inference
            # Use embedded client directly as it has proper object storage configuration
            with TensorZeroGateway.build_embedded(
                clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
                config_file="config/tensorzero.toml",
            ) as client:
                
                response = client.inference(
                    model_name="openai::gpt-4o-mini",
                    input={
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": "Analyze this image and provide a detailed description of what you see. Focus on any text, objects, people, scenes, or concepts that might be relevant for content creation. Be specific and descriptive."
                                    },
                                    {
                                        "type": "file",
                                        "mime_type": mime_type,
                                        "data": image_data
                                    }
                                ]
                            }
                        ]
                    }
                )
                
                # Extract the analysis from the response
                if hasattr(response, 'content') and response.content:
                    analysis = response.content
                elif hasattr(response, 'choices') and response.choices:
                    analysis = response.choices[0].message.content
                else:
                    analysis = str(response)
                
                print(f"✅ Successfully analyzed image")
                print(f"📝 Analysis length: {len(analysis)} characters")
                
                return {
                    "status": "success",
                    "filename": image_path.name,
                    "mime_type": mime_type,
                    "analysis": analysis,
                    "content": f"Image Analysis: {image_path.name}\n\n{analysis}"
                }
                
        except Exception as e:
            print(f"❌ Failed to process image: {e}")
            return {
                "status": "error",
                "error": str(e),
                "content": f"[Image analysis failed: {image_path.name} - {str(e)}]"
            }
    
    def process_image_with_context(self, image_path, context=""):
        """
        Process an image with additional context
        
        Args:
            image_path (str): Path to the image file
            context (str): Additional context for the analysis
            
        Returns:
            dict: Analysis result with description and metadata
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            return {
                "status": "error",
                "error": f"Image file not found: {image_path}",
                "content": f"[Image not found: {image_path}]"
            }
        
        # Processing image with context
        
        try:
            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(image_path))
            if not mime_type or not mime_type.startswith('image/'):
                mime_type = 'image/jpeg'  # Default fallback
            
            # Read and encode image
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Build context-aware prompt
            prompt = "Analyze this image and provide a detailed description of what you see."
            if context:
                prompt += f" Additional context: {context}"
            prompt += " Focus on any text, objects, people, scenes, or concepts that might be relevant for content creation. Be specific and descriptive."
            
            # Use TensorZero Gateway for multimodal inference
            with TensorZeroGateway.build_embedded(
                clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
                config_file="config/tensorzero.toml",
            ) as client:
                
                response = client.inference(
                    model_name="openai::gpt-4o-mini",
                    input={
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    },
                                    {
                                        "type": "file",
                                        "mime_type": mime_type,
                                        "data": image_data
                                    }
                                ]
                            }
                        ]
                    }
                )
                
                # Extract the analysis from the response
                if hasattr(response, 'content') and response.content:
                    analysis = response.content
                elif hasattr(response, 'choices') and response.choices:
                    analysis = response.choices[0].message.content
                else:
                    analysis = str(response)
                
                print(f"✅ Successfully analyzed image with context")
                print(f"📝 Analysis length: {len(analysis)} characters")
                
                return {
                    "status": "success",
                    "filename": image_path.name,
                    "mime_type": mime_type,
                    "context": context,
                    "analysis": analysis,
                    "content": f"Image Analysis: {image_path.name}\n\nContext: {context}\n\nAnalysis: {analysis}"
                }
                
        except Exception as e:
            print(f"❌ Failed to process image: {e}")
            return {
                "status": "error",
                "error": str(e),
                "content": f"[Image analysis failed: {image_path.name} - {str(e)}]"
            }

# Example usage and testing
if __name__ == "__main__":
    processor = MultimodalImageProcessor()
    
    # Test with the image file
    test_image = "sources/1-3.jpg"
    if os.path.exists(test_image):
        print("🧪 Testing multimodal image processing")
        print("=" * 50)
        
        result = processor.process_image(test_image)
        print(f"\nResult: {result['status']}")
        if result['status'] == 'success':
            print(f"Analysis: {result['analysis'][:200]}...")
        else:
            print(f"Error: {result['error']}")
    else:
        print(f"❌ Test image not found: {test_image}")
