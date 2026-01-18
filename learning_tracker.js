/**
 * Learning Tracker - Interactive progress tracking for training modules
 * Features: Section checkboxes, personal notes, localStorage persistence
 */

class LearningTracker {
    constructor(moduleName) {
        this.moduleName = moduleName;
        this.storageKey = `learning_tracker_${moduleName}`;
        this.data = this.loadData();
        this.init();
    }

    loadData() {
        const stored = localStorage.getItem(this.storageKey);
        return stored ? JSON.parse(stored) : { sections: {}, lastUpdated: null };
    }

    saveData() {
        this.data.lastUpdated = new Date().toISOString();
        localStorage.setItem(this.storageKey, JSON.stringify(this.data));
    }

    init() {
        this.injectStyles();
        this.createUI();
        this.attachToSections();
        this.updateProgress();
    }

    injectStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Learning Tracker Styles */
            .learning-tracker-toggle {
                position: fixed;
                bottom: 80px;
                right: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 20px;
                border-radius: 50px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                font-weight: bold;
                display: flex;
                align-items: center;
                gap: 10px;
                z-index: 999;
                transition: transform 0.2s, box-shadow 0.2s;
                border: none;
                font-size: 14px;
            }

            .learning-tracker-toggle:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }

            .learning-tracker-panel {
                position: fixed;
                top: 0;
                right: -400px;
                width: 400px;
                height: 100vh;
                background: white;
                box-shadow: -4px 0 20px rgba(0, 0, 0, 0.15);
                z-index: 1000;
                transition: right 0.3s ease;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
            }

            .learning-tracker-panel.open {
                right: 0;
            }

            .learning-tracker-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                position: sticky;
                top: 0;
                z-index: 10;
            }

            .learning-tracker-header h3 {
                margin: 0 0 15px 0;
                font-size: 1.3em;
            }

            .learning-tracker-close {
                position: absolute;
                top: 15px;
                right: 15px;
                background: rgba(255, 255, 255, 0.2);
                border: none;
                color: white;
                width: 30px;
                height: 30px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 18px;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background 0.2s;
            }

            .learning-tracker-close:hover {
                background: rgba(255, 255, 255, 0.3);
            }

            .progress-bar-container {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                height: 8px;
                overflow: hidden;
                margin-top: 10px;
            }

            .progress-bar-fill {
                background: #10b981;
                height: 100%;
                transition: width 0.3s ease;
                border-radius: 10px;
            }

            .progress-text {
                font-size: 0.9em;
                margin-top: 5px;
                opacity: 0.9;
            }

            .learning-tracker-content {
                padding: 20px;
                flex: 1;
            }

            .learning-tracker-actions {
                padding: 15px 20px;
                border-top: 1px solid #e2e8f0;
                background: #f8fafc;
                display: flex;
                gap: 10px;
            }

            .learning-tracker-actions button {
                flex: 1;
                padding: 10px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.2s;
            }

            .btn-export {
                background: #3b82f6;
                color: white;
            }

            .btn-export:hover {
                background: #2563eb;
            }

            .btn-reset {
                background: #ef4444;
                color: white;
            }

            .btn-reset:hover {
                background: #dc2626;
            }

            .section-item {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 12px;
                transition: all 0.2s;
            }

            .section-item:hover {
                border-color: #667eea;
                box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
            }

            .section-item.understood {
                background: #f0fdf4;
                border-color: #10b981;
            }

            .section-header {
                display: flex;
                align-items: center;
                gap: 10px;
                margin-bottom: 10px;
            }

            .section-checkbox {
                width: 20px;
                height: 20px;
                cursor: pointer;
                accent-color: #10b981;
            }

            .section-title {
                flex: 1;
                font-weight: 600;
                color: #1e293b;
                font-size: 0.95em;
                cursor: pointer;
            }

            .section-item.understood .section-title {
                color: #10b981;
            }

            .notes-toggle {
                background: #f59e0b;
                color: white;
                border: none;
                padding: 5px 12px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 0.85em;
                transition: background 0.2s;
            }

            .notes-toggle:hover {
                background: #d97706;
            }

            .notes-toggle.has-notes {
                background: #8b5cf6;
            }

            .notes-toggle.has-notes:hover {
                background: #7c3aed;
            }

            .notes-area {
                display: none;
                margin-top: 10px;
            }

            .notes-area.open {
                display: block;
            }

            .notes-area textarea {
                width: 100%;
                min-height: 80px;
                padding: 10px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-family: inherit;
                font-size: 0.9em;
                resize: vertical;
            }

            .notes-area textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }

            .section-indicator {
                display: inline-block;
                width: 8px;
                height: 8px;
                border-radius: 50%;
                margin-left: 5px;
            }

            .section-indicator.understood {
                background: #10b981;
            }

            .section-indicator.has-notes {
                background: #f59e0b;
            }

            /* In-page section indicators */
            h2[data-section-id] {
                position: relative;
            }

            h2[data-section-id]::before {
                content: '';
                position: absolute;
                left: -25px;
                top: 50%;
                transform: translateY(-50%);
                width: 12px;
                height: 12px;
                border-radius: 50%;
                border: 2px solid #cbd5e1;
                background: white;
                transition: all 0.2s;
            }

            h2[data-section-id].understood::before {
                background: #10b981;
                border-color: #10b981;
            }

            h2[data-section-id].has-notes::after {
                content: '📝';
                position: absolute;
                left: -25px;
                top: calc(50% + 15px);
                font-size: 12px;
            }

            .empty-state {
                text-align: center;
                padding: 40px 20px;
                color: #64748b;
            }

            .empty-state-icon {
                font-size: 3em;
                margin-bottom: 10px;
            }
        `;
        document.head.appendChild(style);
    }

    createUI() {
        // Toggle button
        const toggle = document.createElement('button');
        toggle.className = 'learning-tracker-toggle';
        toggle.innerHTML = '<span>📚</span> Learning Progress';
        toggle.onclick = () => this.togglePanel();
        document.body.appendChild(toggle);

        // Panel
        const panel = document.createElement('div');
        panel.className = 'learning-tracker-panel';
        panel.id = 'learning-tracker-panel';
        
        panel.innerHTML = `
            <div class="learning-tracker-header">
                <button class="learning-tracker-close" onclick="document.getElementById('learning-tracker-panel').classList.remove('open')">×</button>
                <h3>📚 Learning Progress</h3>
                <div class="progress-bar-container">
                    <div class="progress-bar-fill" id="progress-bar-fill"></div>
                </div>
                <div class="progress-text" id="progress-text">0% Complete</div>
            </div>
            <div class="learning-tracker-content" id="tracker-content"></div>
            <div class="learning-tracker-actions">
                <button class="btn-export" onclick="learningTracker.exportNotes()">📤 Export</button>
                <button class="btn-reset" onclick="learningTracker.resetProgress()">🔄 Reset</button>
            </div>
        `;
        
        document.body.appendChild(panel);
    }

    togglePanel() {
        const panel = document.getElementById('learning-tracker-panel');
        panel.classList.toggle('open');
    }

    attachToSections() {
        const sections = document.querySelectorAll('h2');
        const content = document.getElementById('tracker-content');
        
        if (sections.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📖</div>
                    <p>No sections found in this module.</p>
                </div>
            `;
            return;
        }

        content.innerHTML = '';
        
        sections.forEach((section, index) => {
            const sectionId = `section_${index}`;
            section.setAttribute('data-section-id', sectionId);
            
            const sectionData = this.data.sections[sectionId] || { understood: false, notes: '' };
            
            // Update section visual indicator
            if (sectionData.understood) {
                section.classList.add('understood');
            }
            if (sectionData.notes) {
                section.classList.add('has-notes');
            }
            
            // Create tracker item
            const item = this.createSectionItem(sectionId, section.textContent, sectionData);
            content.appendChild(item);
        });
    }

    createSectionItem(sectionId, title, data) {
        const item = document.createElement('div');
        item.className = 'section-item';
        if (data.understood) item.classList.add('understood');
        
        item.innerHTML = `
            <div class="section-header">
                <input type="checkbox" class="section-checkbox" ${data.understood ? 'checked' : ''} 
                       data-section-id="${sectionId}">
                <span class="section-title" data-section-id="${sectionId}">${title}</span>
                <button class="notes-toggle ${data.notes ? 'has-notes' : ''}" data-section-id="${sectionId}">
                    ${data.notes ? '📝 Notes' : '+ Note'}
                </button>
            </div>
            <div class="notes-area" data-section-id="${sectionId}">
                <textarea placeholder="Add your notes here...">${data.notes || ''}</textarea>
            </div>
        `;
        
        // Checkbox handler
        const checkbox = item.querySelector('.section-checkbox');
        checkbox.addEventListener('change', (e) => {
            this.toggleUnderstood(sectionId, e.target.checked);
        });
        
        // Title click scrolls to section
        const titleSpan = item.querySelector('.section-title');
        titleSpan.addEventListener('click', () => {
            const section = document.querySelector(`h2[data-section-id="${sectionId}"]`);
            section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            this.togglePanel(); // Close panel after navigation
        });
        
        // Notes toggle
        const notesBtn = item.querySelector('.notes-toggle');
        const notesArea = item.querySelector('.notes-area');
        const textarea = notesArea.querySelector('textarea');
        
        notesBtn.addEventListener('click', () => {
            notesArea.classList.toggle('open');
        });
        
        // Save notes on blur
        textarea.addEventListener('blur', () => {
            this.saveNotes(sectionId, textarea.value);
        });
        
        return item;
    }

    toggleUnderstood(sectionId, understood) {
        if (!this.data.sections[sectionId]) {
            this.data.sections[sectionId] = { understood: false, notes: '' };
        }
        this.data.sections[sectionId].understood = understood;
        this.saveData();
        
        // Update UI
        const section = document.querySelector(`h2[data-section-id="${sectionId}"]`);
        const item = document.querySelector(`.section-item .section-checkbox[data-section-id="${sectionId}"]`).closest('.section-item');
        
        if (understood) {
            section.classList.add('understood');
            item.classList.add('understood');
        } else {
            section.classList.remove('understood');
            item.classList.remove('understood');
        }
        
        this.updateProgress();
    }

    saveNotes(sectionId, notes) {
        if (!this.data.sections[sectionId]) {
            this.data.sections[sectionId] = { understood: false, notes: '' };
        }
        this.data.sections[sectionId].notes = notes;
        this.saveData();
        
        // Update button style
        const notesBtn = document.querySelector(`.notes-toggle[data-section-id="${sectionId}"]`);
        const section = document.querySelector(`h2[data-section-id="${sectionId}"]`);
        
        if (notes) {
            notesBtn.classList.add('has-notes');
            notesBtn.textContent = '📝 Notes';
            section.classList.add('has-notes');
        } else {
            notesBtn.classList.remove('has-notes');
            notesBtn.textContent = '+ Note';
            section.classList.remove('has-notes');
        }
    }

    updateProgress() {
        const totalSections = Object.keys(this.data.sections).length;
        const understoodSections = Object.values(this.data.sections).filter(s => s.understood).length;
        const percentage = totalSections > 0 ? Math.round((understoodSections / totalSections) * 100) : 0;
        
        const progressBar = document.getElementById('progress-bar-fill');
        const progressText = document.getElementById('progress-text');
        
        if (progressBar) {
            progressBar.style.width = `${percentage}%`;
        }
        if (progressText) {
            progressText.textContent = `${percentage}% Complete (${understoodSections}/${totalSections} sections)`;
        }
    }

    exportNotes() {
        let markdown = `# ${this.moduleName} - Learning Notes\n\n`;
        markdown += `Generated: ${new Date().toLocaleString()}\n\n`;
        markdown += `Progress: ${Object.values(this.data.sections).filter(s => s.understood).length}/${Object.keys(this.data.sections).length} sections understood\n\n`;
        markdown += `---\n\n`;
        
        const sections = document.querySelectorAll('h2[data-section-id]');
        sections.forEach((section) => {
            const sectionId = section.getAttribute('data-section-id');
            const sectionData = this.data.sections[sectionId];
            
            if (sectionData && (sectionData.understood || sectionData.notes)) {
                markdown += `## ${section.textContent}\n\n`;
                markdown += `**Status:** ${sectionData.understood ? '✅ Understood' : '⏳ In Progress'}\n\n`;
                
                if (sectionData.notes) {
                    markdown += `**Notes:**\n${sectionData.notes}\n\n`;
                }
                
                markdown += `---\n\n`;
            }
        });
        
        // Download as file
        const blob = new Blob([markdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.moduleName}_notes.md`;
        a.click();
        URL.revokeObjectURL(url);
    }

    resetProgress() {
        if (confirm('Are you sure you want to reset all progress for this module? This cannot be undone.')) {
            this.data = { sections: {}, lastUpdated: null };
            this.saveData();
            
            // Remove all visual indicators
            document.querySelectorAll('h2[data-section-id]').forEach(section => {
                section.classList.remove('understood', 'has-notes');
            });
            
            // Refresh UI
            this.attachToSections();
            this.updateProgress();
        }
    }
}

// Auto-initialize when script is loaded
// Module name is extracted from page title or can be set via data attribute
let learningTracker;
document.addEventListener('DOMContentLoaded', () => {
    const moduleName = document.body.getAttribute('data-module-name') || 
                      document.title.replace(/[^a-zA-Z0-9]/g, '_').toLowerCase();
    learningTracker = new LearningTracker(moduleName);
});
