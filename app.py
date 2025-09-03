import os
import logging
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from services.parallel_search import ParallelSearchService
from services.openai_service import OpenAIService

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "medical-search-secret-key")

# Initialize services
parallel_search = ParallelSearchService()
openai_service = OpenAIService()

@app.route('/')
def index():
    """Main page with search interface"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handle medical search queries"""
    try:
        query = request.form.get('query', '').strip()
        
        if not query:
            flash('Please enter a medical question or search term.', 'warning')
            return redirect(url_for('index'))
        
        # Log the search query
        app.logger.info(f"Processing medical search query: {query}")
        
        # Check if query is too long and suggest simplification
        if len(query) > 200:
            flash('Your search query is quite long. For better results, try using shorter, more specific medical terms.', 'warning')
            return redirect(url_for('index'))
        
        # Perform parallel.ai search for medical literature
        try:
            search_results = parallel_search.search_medical_literature(query)
        except Exception as search_error:
            app.logger.error(f"Search API error: {str(search_error)}")
            flash('Search service is temporarily unavailable. Please try again with a simpler query.', 'error')
            return redirect(url_for('index'))
        
        if not search_results:
            flash('No medical literature found for your query. Please try different terms.', 'info')
            return redirect(url_for('index'))
        
        # Process results with OpenAI for better medical context
        enhanced_results = []
        for result in search_results:
            try:
                # Generate medical summary and extract key points
                summary = openai_service.generate_medical_summary(result['content'], query)
                credibility_score = openai_service.assess_medical_credibility(result)
                
                enhanced_result = {
                    'title': result['title'],
                    'url': result['url'],
                    'content': result['content'][:500] + '...' if len(result['content']) > 500 else result['content'],
                    'summary': summary,
                    'credibility_score': credibility_score,
                    'source_type': result.get('source_type', 'Medical Literature'),
                    'publication_date': result.get('publication_date', 'Unknown')
                }
                enhanced_results.append(enhanced_result)
            except Exception as e:
                app.logger.error(f"Error processing result: {str(e)}")
                # Include result even if enhancement fails
                enhanced_results.append({
                    'title': result['title'],
                    'url': result['url'],
                    'content': result['content'][:500] + '...' if len(result['content']) > 500 else result['content'],
                    'summary': 'Summary unavailable',
                    'credibility_score': 'Unknown',
                    'source_type': result.get('source_type', 'Medical Literature'),
                    'publication_date': result.get('publication_date', 'Unknown')
                })
        
        return render_template('search_results.html', 
                             query=query, 
                             results=enhanced_results, 
                             total_results=len(enhanced_results))
        
    except Exception as e:
        app.logger.error(f"Search error: {str(e)}")
        flash('An error occurred while searching medical literature. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for AJAX search requests"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        # Perform search
        search_results = parallel_search.search_medical_literature(query)
        
        # Process with OpenAI
        enhanced_results = []
        for result in search_results[:5]:  # Limit to top 5 for API
            try:
                summary = openai_service.generate_medical_summary(result['content'], query)
                credibility_score = openai_service.assess_medical_credibility(result)
                
                enhanced_results.append({
                    'title': result['title'],
                    'url': result['url'],
                    'summary': summary,
                    'credibility_score': credibility_score,
                    'source_type': result.get('source_type', 'Medical Literature')
                })
            except Exception as e:
                app.logger.error(f"Error processing API result: {str(e)}")
                continue
        
        return jsonify({
            'query': query,
            'results': enhanced_results,
            'total_results': len(enhanced_results)
        })
        
    except Exception as e:
        app.logger.error(f"API search error: {str(e)}")
        return jsonify({'error': 'Search service temporarily unavailable'}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    """API endpoint for content summarization"""
    try:
        data = request.get_json()
        content = data.get('content', '')
        context = data.get('context', '')
        
        if not content:
            return jsonify({'error': 'Content parameter is required'}), 400
        
        summary = openai_service.generate_medical_summary(content, context)
        
        return jsonify({
            'summary': summary,
            'status': 'success'
        })
        
    except Exception as e:
        app.logger.error(f"Summarization error: {str(e)}")
        return jsonify({'error': 'Summarization service temporarily unavailable'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    app.logger.error(f"Internal server error: {str(error)}")
    flash('An internal error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
