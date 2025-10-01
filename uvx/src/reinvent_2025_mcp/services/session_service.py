import json

class SessionService:
    def __init__(self, sessions):
        self.sessions = sessions

    def search_sessions(self, query, limit=20, cursor=0):
        if not query.strip():
            # Return all sessions when query is empty
            results = self.sessions
        else:
            results = [s for s in self.sessions if 
                      query.lower() in (s.get('title', '') or '').lower() or
                      query.lower() in (s.get('abstract', '') or '').lower() or
                      self._search_in_speakers(s.get('speakers', []), query)]
        return self._paginate(results, limit, cursor)

    def search_services(self, query, limit=20, cursor=0):
        all_services = list(set(service for s in self.sessions 
                               for service in s.get('attributes', {}).get('services', [])))
        results = [{'name': service, 'sessionCount': sum(1 for s in self.sessions 
                   if service in s.get('attributes', {}).get('services', []))}
                  for service in all_services if query.lower() in service.lower()]
        return self._paginate(results, limit, cursor)

    def get_session_details(self, session_code):
        session = next((s for s in self.sessions if s.get('code') == session_code), None)
        return self._clean_session_details(session) if session else None

    def list_categories(self, category):
        category_map = {
            'topics': 'topics', 'services': 'services', 'industries': 'industries',
            'roles': 'roles', 'levels': 'level', 'segments': 'segments',
            'areas_of_interest': 'areas_of_interest', 'features': 'features', 'types': 'type'
        }
        
        field = category_map.get(category)
        if not field:
            return []

        if field in ['level', 'type']:
            values = list(set(item for s in self.sessions 
                            for item in s.get('attributes', {}).get(field, [])))
        else:
            values = list(set(item for s in self.sessions 
                            for item in s.get('attributes', {}).get(field, [])))
        
        return [{'name': value, 
                'count': sum(1 for s in self.sessions 
                           if value in s.get('attributes', {}).get(field, [])),
                'percentage': f"{sum(1 for s in self.sessions if value in s.get('attributes', {}).get(field, [])) / len(self.sessions) * 100:.2f}"}
               for value in values]

    def get_sessions_by_service(self, service_name, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if service_name in s.get('attributes', {}).get('services', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_level(self, level, limit=20, cursor=0):
        level_map = {
            '100': '100 – Foundational', '200': '200 – Intermediate', 
            '300': '300 – Advanced', '400': '400 – Expert', '500': '500 – Distinguished'
        }
        full_level = level_map.get(level)
        results = [s for s in self.sessions 
                  if full_level in s.get('attributes', {}).get('level', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_role(self, role, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if role in s.get('attributes', {}).get('roles', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_industry(self, industry, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if industry in s.get('attributes', {}).get('industries', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_segment(self, segment, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if segment in s.get('attributes', {}).get('segments', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_feature(self, feature, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if feature in s.get('attributes', {}).get('features', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_topic(self, topic, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if topic in s.get('attributes', {}).get('topics', [])]
        return self._paginate(results, limit, cursor)

    def get_sessions_by_area_of_interest(self, area_of_interest, limit=20, cursor=0):
        results = [s for s in self.sessions 
                  if area_of_interest in s.get('attributes', {}).get('areas_of_interest', [])]
        return self._paginate(results, limit, cursor)

    def search_speakers(self, speaker_name, limit=5, cursor=0):
        if not speaker_name.strip():
            # Return all speakers when speaker_name is empty
            all_speakers = self._get_all_speakers()
        else:
            all_speakers = self._get_all_speakers()
            all_speakers = [s for s in all_speakers if speaker_name.lower() in s['name'].lower()]
        
        return self._paginate_speakers(all_speakers, limit, cursor)

    def _get_all_speakers(self):
        speaker_sessions = {}
        
        for session in self.sessions:
            speakers = session.get('speakers', [])
            if not speakers:
                continue
                
            for speaker in speakers:
                if isinstance(speaker, str):
                    name = speaker
                    speaker_key = name
                    speaker_info = {'name': name, 'jobTitle': None, 'company': None, 'role': None}
                elif isinstance(speaker, dict):
                    name = (speaker.get('fullName') or speaker.get('globalFullName') or 
                           f"{speaker.get('firstName', '')} {speaker.get('lastName', '')}").strip()
                    if not name:
                        continue
                    speaker_key = name
                    speaker_info = {
                        'name': name,
                        'jobTitle': speaker.get('jobTitle') or speaker.get('globalJobtitle'),
                        'company': speaker.get('companyName') or speaker.get('globalCompany'),
                        'role': speaker.get('roles')
                    }
                else:
                    continue
                
                if speaker_key not in speaker_sessions:
                    speaker_sessions[speaker_key] = {
                        **speaker_info,
                        'sessions': []
                    }
                
                speaker_sessions[speaker_key]['sessions'].append({
                    'code': session.get('code'),
                    'title': session.get('title')
                })
        
        return list(speaker_sessions.values())

    def _paginate_speakers(self, speakers, limit, cursor):
        start = int(cursor) if cursor else 0
        end = start + limit
        items = speakers[start:end]
        
        return {
            'speakers': items,
            'total': len(speakers),
            'hasMore': end < len(speakers),
            'nextCursor': str(end) if end < len(speakers) else None
        }

    def _search_in_speakers(self, speakers, query):
        if not speakers:
            return False
        for speaker in speakers:
            if isinstance(speaker, str):
                if query.lower() in speaker.lower():
                    return True
            elif isinstance(speaker, dict):
                name = (speaker.get('fullName') or speaker.get('globalFullName') or 
                       f"{speaker.get('firstName', '')} {speaker.get('lastName', '')}").strip()
                if query.lower() in name.lower():
                    return True
        return False

    def _paginate(self, results, limit, cursor):
        start = int(cursor) if cursor else 0
        end = start + limit
        items = results[start:end]
        
        return {
            'items': [item if isinstance(item, dict) and 'name' in item 
                     else self._to_minimal_session(item) for item in items],
            'total': len(results),
            'hasMore': end < len(results),
            'nextCursor': str(end) if end < len(results) else None
        }

    def _to_minimal_session(self, session):
        return {
            'code': session.get('code'),
            'title': session.get('title'),
            'abstract': session.get('abstract')
        }

    def _clean_session_details(self, session):
        if not session:
            return None
            
        cleaned = session.copy()
        
        # Remove unwanted fields
        for field in ['length', 'sessionID', 'eventId', 'published', 'modified']:
            cleaned.pop(field, None)
        
        # Clean speakers
        if 'speakers' in cleaned and isinstance(cleaned['speakers'], list):
            cleaned['speakers'] = [
                {
                    'name': (speaker.get('fullName') or speaker.get('globalFullName') or 
                           f"{speaker.get('firstName', '')} {speaker.get('lastName', '')}").strip(),
                    'jobTitle': speaker.get('jobTitle') or speaker.get('globalJobtitle'),
                    'company': speaker.get('companyName') or speaker.get('globalCompany'),
                    'role': speaker.get('roles')
                } if isinstance(speaker, dict) else speaker
                for speaker in cleaned['speakers']
                if speaker and (isinstance(speaker, str) or 
                              (isinstance(speaker, dict) and 
                               (speaker.get('fullName') or speaker.get('globalFullName') or 
                                speaker.get('firstName') or speaker.get('lastName'))))
            ]
        
        return cleaned
