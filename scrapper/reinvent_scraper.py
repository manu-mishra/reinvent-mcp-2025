from playwright.sync_api import sync_playwright
import json
import time

def scrape_all_sessions_comprehensive():
    all_sessions = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        def handle_response(response):
            if 'catalog.awsevents.com/api/search' in response.url:
                try:
                    data = response.json()
                    if data.get('responseCode') == '0':
                        if 'sectionList' in data:
                            for section in data['sectionList']:
                                items = section.get('items', [])
                                all_sessions.extend(items)
                        elif 'items' in data:
                            all_sessions.extend(data['items'])
                        
                        total = data.get('totalSearchItems') or data.get('total', 0)
                        print(f"Sessions: {len(all_sessions)}/{total}")
                        
                except Exception as e:
                    print(f"Error: {e}")
        
        page.on('response', handle_response)
        
        page.goto("https://registration.awsevents.com/flow/awsevents/reinvent2025/eventcatalog/page/eventcatalog")
        page.wait_for_load_state('networkidle')
        time.sleep(5)
        
        # Load all sessions
        for i in range(50):
            show_more = page.locator('button:has-text("Show more")')
            if show_more.count() == 0:
                break
            
            try:
                show_more.first.click()
                time.sleep(2)
            except:
                break
        
        browser.close()
    
    # Process sessions with structured attributes
    processed_sessions = []
    
    for session in all_sessions:
        # Basic session info
        processed_session = {
            'code': session.get('code'),
            'title': session.get('title'),
            'abstract': session.get('abstract'),
            'type': session.get('type'),
            'length': session.get('length'),
            'sessionID': session.get('sessionID'),
            'eventId': session.get('eventId'),
            'published': session.get('published'),
            'modified': session.get('modified')
        }
        
        # Structure attributes by type
        attributes = {
            'type': [],
            'level': [],
            'features': [],
            'topics': [],
            'roles': [],
            'services': [],
            'industries': [],
            'segments': [],
            'areas_of_interest': []
        }
        
        for attr in session.get('attributevalues', []):
            attr_id = attr.get('attribute_id', '').lower()
            value = attr.get('value')
            
            if attr_id == 'type':
                attributes['type'].append(value)
            elif attr_id == 'level':
                attributes['level'].append(value)
            elif attr_id == 'features':
                attributes['features'].append(value)
            elif attr_id == 'topic':
                attributes['topics'].append(value)
            elif attr_id == 'role':
                attributes['roles'].append(value)
            elif attr_id == 'services':
                attributes['services'].append(value)
            elif attr_id == 'industry':
                attributes['industries'].append(value)
            elif attr_id == 'segment':
                attributes['segments'].append(value)
            elif attr_id == 'areaofinterest':
                attributes['areas_of_interest'].append(value)
        
        processed_session['attributes'] = attributes
        processed_session['speakers'] = session.get('participants', [])
        
        processed_sessions.append(processed_session)
    
    # Remove duplicates
    unique_sessions = {}
    for session in processed_sessions:
        session_id = session.get('sessionID')
        if session_id:
            unique_sessions[session_id] = session
    
    final_sessions = list(unique_sessions.values())
    
    # Save structured data
    with open('../data/sessions.json', 'w') as f:
        json.dump(final_sessions, f, indent=2)
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Total sessions: {len(final_sessions)}")
    
    # Data quality check
    no_title = len([s for s in final_sessions if not s.get('title')])
    no_abstract = len([s for s in final_sessions if not s.get('abstract')])
    
    print(f"Missing title: {no_title}")
    print(f"Missing abstract: {no_abstract}")
    
    # Show sample structured session
    if final_sessions:
        sample = final_sessions[0]
        print(f"\nSample structured session:")
        print(f"Code: {sample['code']}")
        print(f"Title: {sample['title']}")
        print(f"Roles: {sample['attributes']['roles']}")
        print(f"Topics: {sample['attributes']['topics']}")
        print(f"Level: {sample['attributes']['level']}")

if __name__ == "__main__":
    scrape_all_sessions_comprehensive()
