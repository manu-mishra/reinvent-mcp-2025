export class SessionService {
  constructor(sessions) {
    this.sessions = sessions;
  }

  searchSessions(query, limit = 20, cursor = 0) {
    let results;
    if (!query.trim()) {
      // Return all sessions when query is empty
      results = this.sessions;
    } else {
      results = this.sessions.filter(session => 
        session.title?.toLowerCase().includes(query.toLowerCase()) ||
        session.abstract?.toLowerCase().includes(query.toLowerCase()) ||
        this.searchInSpeakers(session.speakers, query)
      );
    }
    
    return this.paginate(results, limit, cursor);
  }

  searchServices(query, limit = 20, cursor = 0) {
    const allServices = [...new Set(this.sessions.flatMap(s => s.attributes?.services || []))];
    const results = allServices
      .filter(service => service.toLowerCase().includes(query.toLowerCase()))
      .map(service => ({
        name: service,
        sessionCount: this.sessions.filter(s => s.attributes?.services?.includes(service)).length
      }));
    
    return this.paginate(results, limit, cursor);
  }

  getSessionDetails(sessionCode) {
    const session = this.sessions.find(s => s.code === sessionCode);
    if (!session) return null;
    
    return this.cleanSessionDetails(session);
  }

  cleanSessionDetails(session) {
    const cleaned = { ...session };
    
    // Remove unwanted top-level fields
    delete cleaned.length;
    delete cleaned.sessionID;
    delete cleaned.eventId;
    delete cleaned.published;
    delete cleaned.modified;
    
    // Clean speakers array - keep only essential fields
    if (cleaned.speakers && Array.isArray(cleaned.speakers)) {
      cleaned.speakers = cleaned.speakers.map(speaker => {
        if (typeof speaker === 'string') return speaker;
        if (typeof speaker === 'object') {
          return {
            name: speaker.fullName || speaker.globalFullName || `${speaker.firstName || ''} ${speaker.lastName || ''}`.trim(),
            jobTitle: speaker.jobTitle || speaker.globalJobtitle,
            company: speaker.companyName || speaker.globalCompany,
            role: speaker.roles
          };
        }
        return speaker;
      }).filter(speaker => speaker && (typeof speaker === 'string' || speaker.name));
    }
    
    return cleaned;
  }

  listCategories(category) {
    const categoryMap = {
      topics: 'attributes.topics',
      services: 'attributes.services', 
      industries: 'attributes.industries',
      roles: 'attributes.roles',
      levels: 'attributes.level',
      segments: 'attributes.segments',
      areas_of_interest: 'attributes.areas_of_interest',
      features: 'attributes.features',
      types: 'attributes.type'
    };

    const field = categoryMap[category];
    if (!field) return [];

    if (field === 'attributes.level' || field === 'attributes.type') {
      // Single value fields - extract from arrays
      const values = [...new Set(this.sessions.flatMap(s => s.attributes?.[field.split('.')[1]] || []))];
      return values.map(value => ({
        name: value,
        count: this.sessions.filter(s => s.attributes?.[field.split('.')[1]]?.includes(value)).length,
        percentage: ((this.sessions.filter(s => s.attributes?.[field.split('.')[1]]?.includes(value)).length / this.sessions.length) * 100).toFixed(2)
      }));
    } else {
      // Array fields
      const fieldName = field.split('.')[1];
      const values = [...new Set(this.sessions.flatMap(s => s.attributes?.[fieldName] || []))];
      return values.map(value => ({
        name: value,
        count: this.sessions.filter(s => s.attributes?.[fieldName]?.includes(value)).length,
        percentage: ((this.sessions.filter(s => s.attributes?.[fieldName]?.includes(value)).length / this.sessions.length) * 100).toFixed(2)
      }));
    }
  }

  getSessionsByService(serviceName, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.services?.includes(serviceName));
    return this.paginate(results, limit, cursor);
  }

  getSessionsByLevel(level, limit = 20, cursor = 0) {
    const levelMap = {
      '100': '100 – Foundational',
      '200': '200 – Intermediate', 
      '300': '300 – Advanced',
      '400': '400 – Expert',
      '500': '500 – Distinguished'
    };
    const fullLevel = levelMap[level];
    const results = this.sessions.filter(s => s.attributes?.level?.includes(fullLevel));
    return this.paginate(results, limit, cursor);
  }

  getSessionsByRole(role, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.roles?.includes(role));
    return this.paginate(results, limit, cursor);
  }

  getSessionsByIndustry(industry, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.industries?.includes(industry));
    return this.paginate(results, limit, cursor);
  }

  getSessionsBySegment(segment, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.segments?.includes(segment));
    return this.paginate(results, limit, cursor);
  }

  getSessionsByFeature(feature, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.features?.includes(feature));
    return this.paginate(results, limit, cursor);
  }

  getSessionsByTopic(topic, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.topics?.includes(topic));
    return this.paginate(results, limit, cursor);
  }

  getSessionsByAreaOfInterest(areaOfInterest, limit = 20, cursor = 0) {
    const results = this.sessions.filter(s => s.attributes?.areas_of_interest?.includes(areaOfInterest));
    return this.paginate(results, limit, cursor);
  }

  searchSpeakers(speakerName, limit = 5, cursor = 0) {
    let allSpeakers;
    if (!speakerName.trim()) {
      // Return all speakers when speakerName is empty
      allSpeakers = this.getAllSpeakers();
    } else {
      allSpeakers = this.getAllSpeakers();
      allSpeakers = allSpeakers.filter(s => 
        s.name.toLowerCase().includes(speakerName.toLowerCase())
      );
    }
    
    return this.paginateSpeakers(allSpeakers, limit, cursor);
  }

  getAllSpeakers() {
    const speakerSessions = {};
    
    for (const session of this.sessions) {
      const speakers = session.speakers || [];
      if (!speakers.length) continue;
      
      for (const speaker of speakers) {
        let name, speakerKey, speakerInfo;
        
        if (typeof speaker === 'string') {
          name = speaker;
          speakerKey = name;
          speakerInfo = { name, jobTitle: null, company: null, role: null };
        } else if (typeof speaker === 'object') {
          name = (speaker.fullName || speaker.globalFullName || 
                 `${speaker.firstName || ''} ${speaker.lastName || ''}`.trim());
          if (!name) continue;
          speakerKey = name;
          speakerInfo = {
            name,
            jobTitle: speaker.jobTitle || speaker.globalJobtitle,
            company: speaker.companyName || speaker.globalCompany,
            role: speaker.roles
          };
        } else {
          continue;
        }
        
        if (!speakerSessions[speakerKey]) {
          speakerSessions[speakerKey] = {
            ...speakerInfo,
            sessions: []
          };
        }
        
        speakerSessions[speakerKey].sessions.push({
          code: session.code,
          title: session.title
        });
      }
    }
    
    return Object.values(speakerSessions);
  }

  paginateSpeakers(speakers, limit, cursor) {
    const start = parseInt(cursor) || 0;
    const end = start + limit;
    const items = speakers.slice(start, end);
    
    return {
      speakers: items,
      total: speakers.length,
      hasMore: end < speakers.length,
      nextCursor: end < speakers.length ? String(end) : null
    };
  }

  searchInSpeakers(speakers, query) {
    if (!speakers || !Array.isArray(speakers)) return false;
    
    return speakers.some(speaker => {
      if (typeof speaker === 'string') {
        return speaker.toLowerCase().includes(query.toLowerCase());
      }
      if (typeof speaker === 'object') {
        const name = speaker.fullName || speaker.globalFullName || `${speaker.firstName || ''} ${speaker.lastName || ''}`.trim();
        return name.toLowerCase().includes(query.toLowerCase());
      }
      return false;
    });
  }

  paginate(results, limit, cursor) {
    const start = parseInt(cursor) || 0;
    const end = start + limit;
    const items = results.slice(start, end);
    
    return {
      items: items.map(item => item.name ? item : this.toMinimalSession(item)),
      total: results.length,
      hasMore: end < results.length,
      nextCursor: end < results.length ? end.toString() : null
    };
  }

  toMinimalSession(session) {
    return {
      code: session.code,
      title: session.title,
      abstract: session.abstract
    };
  }
}
