class FacilitiesManagementHub {
    constructor() {
        this.currentProvider = null;
        this.init();
    }

    init() {
        this.loadDashboardData();
        this.setupEventListeners();
        this.updateDateTime();
        setInterval(() => this.updateDateTime(), 60000); // Update every minute
    }

    setupEventListeners() {
        // Mobile menu toggle if exists
        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
        if (mobileMenuBtn) {
            mobileMenuBtn.addEventListener('click', this.toggleMobileMenu.bind(this));
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            const sidebar = document.getElementById('sidebar');
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            if (sidebar && !sidebar.contains(e.target) && !mobileMenuBtn?.contains(e.target)) {
                this.closeMobileMenu();
            }
        });

        // Touch events for mobile
        this.setupTouchEvents();
    }

    setupTouchEvents() {
        // Prevent zoom on double tap for better mobile experience
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    }

    toggleMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.toggle('translate-x-0');
            sidebar.classList.toggle('-translate-x-full');
            overlay.classList.toggle('hidden');
        }
    }

    closeMobileMenu() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        
        if (sidebar && overlay) {
            sidebar.classList.add('-translate-x-full');
            sidebar.classList.remove('translate-x-0');
            overlay.classList.add('hidden');
        }
    }

    updateDateTime() {
        const now = new Date();
        const dateStr = now.toLocaleDateString('en-ZA');
        const auditDateElement = document.getElementById('last-audit-date');
        if (auditDateElement && !auditDateElement.textContent) {
            auditDateElement.textContent = dateStr;
        }
    }

    async loadDashboardData() {
        try {
            // Load dashboard statistics
            const response = await fetch('/api/dashboard/stats');
            if (response.ok) {
                const data = await response.json();
                this.updateDashboardMetrics(data.data);
            }
            
            // Load service provider summary data
            const providerResponse = await fetch('/api/dashboard/service-providers-summary');
            if (providerResponse.ok) {
                const providerData = await providerResponse.json();
                this.updateServiceProviderMetrics(providerData.data);
            }
        } catch (error) {
            console.log('Using static data for dashboard metrics');
            // Use static data as fallback
            this.updateDashboardMetrics({
                overview: {
                    total_tickets: 12,
                    active_assets: 428,
                    total_tools: 15,
                    total_staff: 8
                }
            });
        }
    }

    updateDashboardMetrics(data) {
        // Update stores & infrastructure metrics
        if (data.overview) {
            const storesAssets = document.getElementById('stores-assets');
            const storesWorkorders = document.getElementById('stores-workorders');
            
            if (storesAssets) {
              storesAssets.textContent = data.overview.active_assets || 428;
            }
            if (storesWorkorders) {
              storesWorkorders.textContent = data.overview.total_tickets || 12;
            }
        }
    }

    updateServiceProviderMetrics(data) {
        // Update service provider metrics from API data
        Object.keys(data).forEach(providerCode => {
            const provider = data[providerCode];
            if (provider.metrics) {
                Object.keys(provider.metrics).forEach(metricName => {
                    const elementId = this.getMetricElementId(providerCode, metricName);
                    const element = document.getElementById(elementId);
                    if (element) {
                        element.textContent = provider.metrics[metricName];
                    }
                });
            }
        });
    }

    getMetricElementId(providerCode, metricName) {
        // Convert metric names to element IDs
        const metricMap = {
            'stores': {
                'Assets Under Management': 'stores-assets',
                'Inventory Accuracy': 'stores-accuracy',
                'Active Work Orders': 'stores-workorders',
                'Compliance Score': 'stores-reorders'
            },
            'leitch': {
                'Hours This Week': 'leitch-hours',
                'Tasks Completed': 'leitch-tasks',
                'Active Projects': 'leitch-projects',
                'Client Satisfaction': 'leitch-compliance'
            },
            'sabeliwe': {
                'Hours This Week': 'sabeliwe-hours',
                'Tasks Completed': 'sabeliwe-tasks',
                'Active Projects': 'sabeliwe-projects',
                'Garden Health Score': 'sabeliwe-compliance'
            },
            'csg': {
                'Meals Served Today': 'csg-meals',
                'Customer Satisfaction': 'csg-satisfaction',
                'Special Events': 'csg-events',
                'Food Safety Score': 'csg-compliance'
            },
            'livclean': {
                'Areas Completed': 'livclean-areas',
                'Quality Score': 'livclean-quality',
                'Special Requests': 'livclean-requests',
                'Compliance Rate': 'livclean-compliance'
            }
        };
        
        return metricMap[providerCode]?.[metricName] || null;
    }

    async showProviderContent(provider) {
        this.currentProvider = provider;
        const contentArea = document.getElementById('provider-content');
        
        if (!contentArea) {
          return;
        }

        try {
            // Try to fetch real data from API
            const response = await fetch(`/api/service-providers/${provider}`);
            if (response.ok) {
                const data = await response.json();
                const providerData = this.formatApiProviderData(data.data);
                contentArea.innerHTML = this.generateProviderHTML(providerData);
            } else {
                // Fallback to static data
                const providerData = this.getProviderData(provider);
                contentArea.innerHTML = this.generateProviderHTML(providerData);
            }
        } catch (error) {
            console.log('Using static data for provider content');
            const providerData = this.getProviderData(provider);
            contentArea.innerHTML = this.generateProviderHTML(providerData);
        }
        
        // Scroll to content area on mobile
        if (window.innerWidth < 768) {
            contentArea.scrollIntoView({ behavior: 'smooth' });
        }
    }

    formatApiProviderData(apiData) {
        // Convert API data to the format expected by generateProviderHTML
        return {
            name: apiData.name,
            tagline: apiData.tagline,
            icon: apiData.icon,
            description: apiData.description,
            services: apiData.services.map(service => service.name),
            metrics: apiData.metrics.reduce((acc, metric) => {
                acc[metric.metric_name] = metric.metric_value;
                return acc;
            }, {}),
            recentActivity: apiData.recent_activities.map(activity => activity.description)
        };
    }

    getProviderData(provider) {
        const providers = {
            stores: {
                name: 'STORES & INFRASTRUCTURE',
                tagline: 'Precision Management | ISO 41001 Excellence',
                icon: 'fas fa-warehouse',
                description: 'Comprehensive asset management and infrastructure oversight for Derivco Durban facilities.',
                services: [
                    'Asset Register Management',
                    'Work Order Processing',
                    'Inventory Control',
                    'Compliance Monitoring'
                ],
                metrics: {
                    'Assets Under Management': '428',
                    'Inventory Accuracy': '97.3%',
                    'Active Work Orders': '12',
                    'Compliance Score': '100%'
                },
                recentActivity: [
                    'Asset PROJ-001 registered and tagged',
                    'Work order #WO-2025-001 completed',
                    'Monthly inventory audit completed',
                    'ISO 41001 compliance review passed'
                ]
            },
            leitch: {
                name: 'LEITCH LANDSCAPE',
                tagline: 'Commercial Landscaping Services',
                icon: 'fas fa-tree',
                description: 'Professional landscaping and grounds maintenance services for corporate facilities.',
                services: [
                    'Landscape Design & Installation',
                    'Grounds Maintenance',
                    'Irrigation Systems',
                    'Seasonal Plantings'
                ],
                metrics: {
                    'Hours This Week': '24',
                    'Tasks Completed': '9',
                    'Active Projects': '3',
                    'Client Satisfaction': '98%'
                },
                recentActivity: [
                    'Completed weekly lawn maintenance',
                    'Installed new irrigation system - Block A',
                    'Seasonal flower bed preparation',
                    'Tree pruning and health assessment'
                ]
            },
            sabeliwe: {
                name: 'SABELIWE GARDEN',
                tagline: 'Garden & Property Maintenance',
                icon: 'fas fa-leaf',
                description: 'Specialized garden maintenance and property care services.',
                services: [
                    'Garden Maintenance',
                    'Plant Care & Nurturing',
                    'Pest Control',
                    'Seasonal Garden Planning'
                ],
                metrics: {
                    'Hours This Week': '18',
                    'Tasks Completed': '7',
                    'Active Projects': '2',
                    'Garden Health Score': '95%'
                },
                recentActivity: [
                    'Completed rose garden pruning',
                    'Applied organic fertilizer treatment',
                    'Pest control inspection passed',
                    'New herb garden installation started'
                ]
            },
            csg: {
                name: 'CSG FOODS',
                tagline: 'Canteen & Catering Services',
                icon: 'fas fa-utensils',
                description: 'Professional food service and catering for corporate dining facilities.',
                services: [
                    'Daily Meal Service',
                    'Special Event Catering',
                    'Menu Planning',
                    'Food Safety Compliance'
                ],
                metrics: {
                    'Meals Served Today': '342',
                    'Customer Satisfaction': '94%',
                    'Special Events': '2',
                    'Food Safety Score': '100%'
                },
                recentActivity: [
                    'Served 342 meals today',
                    'Catered executive board meeting',
                    'Weekly menu planning completed',
                    'Food safety audit passed with excellence'
                ]
            },
            livclean: {
                name: 'LIVCLEAN',
                tagline: 'Cleaning & Sanitation Services',
                icon: 'fas fa-broom',
                description: 'Professional cleaning and sanitation services for corporate facilities.',
                services: [
                    'Daily Office Cleaning',
                    'Deep Sanitization',
                    'Restroom Maintenance',
                    'Waste Management'
                ],
                metrics: {
                    'Areas Completed': '98%',
                    'Quality Score': '4.8/5',
                    'Special Requests': '2',
                    'Compliance Rate': '100%'
                },
                recentActivity: [
                    'Completed daily office cleaning rounds',
                    'Deep sanitization of conference rooms',
                    'Restroom supplies restocked',
                    'Quality inspection passed - all areas'
                ]
            }
        };

        return providers[provider] || providers.stores;
    }

    generateProviderHTML(data) {
        return `
            <div class="text-white">
                <div class="flex items-center mb-6">
                    <div class="bg-teal-600 p-3 rounded-full mr-4">
                        <i class="${data.icon} text-white text-2xl"></i>
                    </div>
                    <div>
                        <h3 class="text-2xl font-semibold">${data.name}</h3>
                        <p class="text-teal-400">${data.tagline}</p>
                    </div>
                </div>

                <p class="text-gray-300 mb-6">${data.description}</p>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Services -->
                    <div class="bg-slate-700 p-4 rounded-lg">
                        <h4 class="text-lg font-semibold text-teal-400 mb-4">Services</h4>
                        <ul class="space-y-2">
                            ${data.services.map(service => `
                                <li class="flex items-center">
                                    <i class="fas fa-check text-lime-400 mr-2"></i>
                                    <span>${service}</span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>

                    <!-- Metrics -->
                    <div class="bg-slate-700 p-4 rounded-lg">
                        <h4 class="text-lg font-semibold text-teal-400 mb-4">Key Metrics</h4>
                        <div class="space-y-3">
                            ${Object.entries(data.metrics).map(([key, value]) => `
                                <div class="flex justify-between">
                                    <span class="text-gray-300">${key}</span>
                                    <span class="text-lime-400 font-semibold">${value}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>

                <!-- Recent Activity -->
                <div class="mt-6 bg-slate-700 p-4 rounded-lg">
                    <h4 class="text-lg font-semibold text-teal-400 mb-4">Recent Activity</h4>
                    <div class="space-y-3">
                        ${data.recentActivity.map(activity => `
                            <div class="log-item">
                                <div class="text-sm text-white">${activity}</div>
                                <div class="text-xs text-gray-400">${this.getRandomTimeAgo()}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>

                <!-- Action Buttons -->
                <div class="mt-6 flex flex-wrap gap-3">
                    <button class="btn btn-primary" onclick="facilitiesHub.showProviderModal('${this.currentProvider}', 'schedule')">
                        <i class="fas fa-calendar mr-2"></i>Schedule Service
                    </button>
                    <button class="btn btn-primary" onclick="facilitiesHub.showProviderModal('${this.currentProvider}', 'report')">
                        <i class="fas fa-chart-bar mr-2"></i>View Reports
                    </button>
                    <button class="btn btn-primary" onclick="facilitiesHub.showProviderModal('${this.currentProvider}', 'contact')">
                        <i class="fas fa-phone mr-2"></i>Contact Provider
                    </button>
                </div>
            </div>
        `;
    }

    getRandomTimeAgo() {
        const times = ['2 minutes ago', '15 minutes ago', '1 hour ago', '3 hours ago', 'Earlier today'];
        return times[Math.floor(Math.random() * times.length)];
    }

    showProviderModal(provider, action) {
        const modal = this.createModal();
        const providerData = this.getProviderData(provider);
        
        let modalContent = '';
        
        switch (action) {
            case 'schedule':
                modalContent = this.generateScheduleModalContent(providerData);
                break;
            case 'report':
                modalContent = this.generateReportModalContent(providerData);
                break;
            case 'contact':
                modalContent = this.generateContactModalContent(providerData);
                break;
        }
        
        modal.querySelector('.modal-content').innerHTML = modalContent;
        modal.style.display = 'block';
    }

    generateScheduleModalContent(data) {
        return `
            <h3 class="text-xl font-semibold mb-4 text-gray-800">Schedule Service - ${data.name}</h3>
            <form onsubmit="facilitiesHub.handleScheduleSubmit(event)">
                <div class="form-group">
                    <label class="text-gray-700">Service Type</label>
                    <select class="form-control text-gray-800 bg-white">
                        ${data.services.map(service => `<option value="${service}">${service}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label class="text-gray-700">Preferred Date</label>
                    <input type="date" class="form-control text-gray-800 bg-white" required>
                </div>
                <div class="form-group">
                    <label class="text-gray-700">Preferred Time</label>
                    <input type="time" class="form-control text-gray-800 bg-white" required>
                </div>
                <div class="form-group">
                    <label class="text-gray-700">Special Requirements</label>
                    <textarea class="form-control text-gray-800 bg-white" rows="3" placeholder="Any special requirements or notes..."></textarea>
                </div>
                <div class="flex justify-end gap-3">
                    <button type="button" class="btn bg-gray-500 text-white" onclick="facilitiesHub.closeModal()">Cancel</button>
                    <button type="submit" class="btn btn-primary">Schedule Service</button>
                </div>
            </form>
        `;
    }

    generateReportModalContent(data) {
        return `
            <h3 class="text-xl font-semibold mb-4 text-gray-800">Reports - ${data.name}</h3>
            <div class="space-y-4">
                <div class="bg-gray-100 p-4 rounded">
                    <h4 class="font-semibold text-gray-800">Performance Summary</h4>
                    <div class="mt-2 space-y-2">
                        ${Object.entries(data.metrics).map(([key, value]) => `
                            <div class="flex justify-between text-gray-700">
                                <span>${key}</span>
                                <span class="font-semibold">${value}</span>
                            </div>
                        `).join('')}
                    </div>
                </div>
                <div class="bg-gray-100 p-4 rounded">
                    <h4 class="font-semibold text-gray-800">Recent Activities</h4>
                    <div class="mt-2 space-y-1">
                        ${data.recentActivity.map(activity => `
                            <div class="text-sm text-gray-600">• ${activity}</div>
                        `).join('')}
                    </div>
                </div>
                <div class="flex justify-end gap-3">
                    <button class="btn bg-gray-500 text-white" onclick="facilitiesHub.closeModal()">Close</button>
                    <button class="btn btn-primary" onclick="facilitiesHub.downloadReport('${this.currentProvider}')">Download Report</button>
                </div>
            </div>
        `;
    }

    generateContactModalContent(data) {
        return `
            <h3 class="text-xl font-semibold mb-4 text-gray-800">Contact - ${data.name}</h3>
            <div class="space-y-4">
                <div class="bg-gray-100 p-4 rounded">
                    <h4 class="font-semibold text-gray-800">Contact Information</h4>
                    <div class="mt-2 space-y-2 text-gray-700">
                        <div><i class="fas fa-phone mr-2"></i> +27 31 123 4567</div>
                        <div><i class="fas fa-envelope mr-2"></i> contact@${data.name.toLowerCase().replace(/\s+/g, '')}.co.za</div>
                        <div><i class="fas fa-clock mr-2"></i> Mon-Fri: 8:00 AM - 5:00 PM</div>
                    </div>
                </div>
                <form onsubmit="facilitiesHub.handleContactSubmit(event)">
                    <div class="form-group">
                        <label class="text-gray-700">Subject</label>
                        <input type="text" class="form-control text-gray-800 bg-white" placeholder="Subject" required>
                    </div>
                    <div class="form-group">
                        <label class="text-gray-700">Message</label>
                        <textarea class="form-control text-gray-800 bg-white" rows="4" placeholder="Your message..." required></textarea>
                    </div>
                    <div class="flex justify-end gap-3">
                        <button type="button" class="btn bg-gray-500 text-white" onclick="facilitiesHub.closeModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">Send Message</button>
                    </div>
                </form>
            </div>
        `;
    }

    createModal() {
        let modal = document.getElementById('provider-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'provider-modal';
            modal.className = 'modal';
            modal.innerHTML = '<div class="modal-content"></div>';
            document.body.appendChild(modal);
            
            // Close modal when clicking outside
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal();
                }
            });
        }
        return modal;
    }

    closeModal() {
        const modal = document.getElementById('provider-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }

    handleScheduleSubmit(event) {
        event.preventDefault();
        // Simulate API call
        this.showNotification('Service scheduled successfully!', 'success');
        this.closeModal();
    }

    handleContactSubmit(event) {
        event.preventDefault();
        // Simulate API call
        this.showNotification('Message sent successfully!', 'success');
        this.closeModal();
    }

    downloadReport(provider) {
        // Simulate report download
        this.showNotification('Report download started...', 'info');
        this.closeModal();
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg text-white z-50 ${
            type === 'success' ? 'bg-green-600' : 
            type === 'error' ? 'bg-red-600' : 
            'bg-blue-600'
        }`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// Global functions for onclick handlers
function showProviderContent(provider) {
    facilitiesHub.showProviderContent(provider);
}

// Initialize the application
const facilitiesHub = new FacilitiesManagementHub();

// Make it globally available for onclick handlers
window.facilitiesHub = facilitiesHub;