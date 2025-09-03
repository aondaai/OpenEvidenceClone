import os
import requests
import logging
from typing import List, Dict, Any

class ParallelSearchService:
    """Service for interacting with parallel.ai Search API for medical literature"""
    
    def __init__(self):
        self.api_key = os.environ.get("PARALLEL_API_KEY", "")
        self.base_url = "https://api.parallel.ai/v1beta/search"
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }
        
        if not self.api_key:
            logging.warning("PARALLEL_API_KEY environment variable not set")
    
    def search_medical_literature(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search for medical literature using parallel.ai Search API
        
        Args:
            query: Medical search query
            max_results: Maximum number of results to return
            
        Returns:
            List of search results with medical content
        """
        try:
            if not self.api_key:
                raise Exception("Parallel.ai API key not configured")
            
            # Simplified search queries for better results
            search_queries = [
                f"{query}",
                f"{query} medical",
                f"{query} clinical"
            ]
            
            payload = {
                "objective": f"Find medical information about: {query}",
                "search_queries": search_queries[:2],  # Use top 2 queries
                "processor": "base",
                "max_results": max_results,
                "max_chars_per_result": 1500
            }
            
            logging.info(f"Searching parallel.ai for medical query: {query}")
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                logging.debug(f"Parallel.ai response: {data}")
                results = []
                
                # Process search results
                search_results = data.get('results', [])
                for result in search_results:
                    # Extract content from excerpts array (new API format)
                    excerpts = result.get('excerpts', [])
                    content = ' '.join(excerpts) if excerpts else result.get('content', '')
                    
                    processed_result = {
                        'title': result.get('title', 'Medical Literature'),
                        'url': result.get('url', ''),
                        'content': content,
                        'source_type': self._determine_source_type(result.get('url', '')),
                        'publication_date': result.get('date', 'Unknown'),
                        'relevance_score': result.get('score', 0)
                    }
                    
                    # Only include results with substantial content
                    if len(processed_result['content'].strip()) > 50:  # Lower threshold for excerpts
                        results.append(processed_result)
                
                logging.info(f"Found {len(results)} medical literature results")
                return results
            
            elif response.status_code == 401:
                raise Exception("Invalid Parallel.ai API key")
            elif response.status_code == 429:
                raise Exception("Parallel.ai API rate limit exceeded")
            else:
                logging.error(f"Parallel.ai API error: {response.status_code} - {response.text}")
                raise Exception(f"Search service error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            logging.error("Parallel.ai API timeout")
            raise Exception("Search request timed out. Please try again with a simpler query.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Parallel.ai request error: {str(e)}")
            raise Exception("Unable to connect to search service. Please try again.")
        except Exception as e:
            logging.error(f"Search error: {str(e)}")
            raise Exception(f"Search failed: {str(e)}")
    
    def _determine_source_type(self, url: str) -> str:
        """Determine the type of medical source based on URL"""
        medical_domains = {
            'pubmed.ncbi.nlm.nih.gov': 'PubMed',
            'nejm.org': 'NEJM',
            'jamanetwork.com': 'JAMA',
            'thelancet.com': 'The Lancet',
            'bmj.com': 'BMJ',
            'nature.com': 'Nature',
            'science.org': 'Science',
            'cochranelibrary.com': 'Cochrane',
            'uptodate.com': 'UpToDate',
            'who.int': 'WHO',
            'cdc.gov': 'CDC',
            'nih.gov': 'NIH',
            'mayoclinic.org': 'Mayo Clinic'
        }
        
        url_lower = url.lower()
        for domain, source_name in medical_domains.items():
            if domain in url_lower:
                return source_name
        
        return 'Medical Literature'
    
    def search_specific_medical_topic(self, topic: str, specialty: str = "") -> List[Dict[str, Any]]:
        """
        Search for specific medical topics with optional specialty filter
        
        Args:
            topic: Specific medical topic (disease, treatment, etc.)
            specialty: Medical specialty to focus on
            
        Returns:
            List of specialized medical search results
        """
        specialty_context = f" {specialty}" if specialty else ""
        enhanced_topic = f"{topic}{specialty_context} clinical evidence medical research"
        
        return self.search_medical_literature(enhanced_topic, max_results=8)
