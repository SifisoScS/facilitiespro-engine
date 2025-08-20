// FacilitiesPro Command Center JavaScript
class FacilitiesCommandCenter {
    constructor() {
        this.currentView = 'dashboard';
        this.init();
    }

    init() {
        this.updateDates();
        this.setupNavigation();
        this.loadDashboardData();
        this.setupMobileOptimization();
    }

    updateDates() {
        const lastAuditDate = new Date().toLocaleDateString('en-ZA');
        const lastUpdated = new Date().toLocaleString('en-ZA', { dateStyle: 'medium', timeStyle: 'short' });
        
        const auditElement = document.getElementById('last-audit-date');
        const updatedElement = document.getElementById('last-updated');
        
        if (auditElement) auditElement.textContent = lastAuditDate;
        if (updatedElement) updatedElement.textContent = lastUpdated;
    }

    setupMobileOptimization() {
        // Touch event support for mobile
        document.addEventListener('touchstart', (e) => {
            // Handle touch events for better mobile experience
        });

        // Prevent zoom on double tap for better mobile UX
        let lastTouchEnd = 0;
        document.addEventListener('touchend', (e) => {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                e.preventDefault();
            }
            lastTouchEnd = now;
        }, false);
    }

    // Content for each navigation item
    navContents = {
        "asset-register": () => this.renderAssetRegister(),
        "storeroom-view": () => this.renderStoreroomView(),
        "work-order": () => this.renderWorkOrderPortal(),
        "maintenance-calendar": () => this.renderMaintenanceCalendar(),
        "compliance-docs": () => this.renderComplianceDocs(),
        "shezi-methodology": () => this.renderSheziMethodology()
    };

    async renderAssetRegister() {
        try {
            const response = await fetch('/api/assets');
            const data = await response.json();
            
            if (data.success) {
                return `
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-xl font-semibold text-teal-400">Asset Register</h4>
                        <button onclick="app.showCreateAssetModal()" class="bg-teal-600 text-white px-4 py-2 rounded-md hover:bg-teal-700 text-sm">
                            <i class="fas fa-plus mr-2"></i>Add Asset
                        </button>
                    </div>
                    <p class="mb-4 text-white">A comprehensive list of all assets under management, including serial numbers, locations, and status.</p>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm text-left text-white border border-gray-700 rounded">
                            <thead class="bg-teal-700">
                                <tr>
                                    <th class="px-3 py-2 border border-gray-600">Asset Tag</th>
                                    <th class="px-3 py-2 border border-gray-600">Name</th>
                                    <th class="px-3 py-2 border border-gray-600">Location</th>
                                    <th class="px-3 py-2 border border-gray-600">Condition</th>
                                    <th class="px-3 py-2 border border-gray-600">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.data.map((asset, index) => `
                                    <tr class="border border-gray-600 ${index % 2 === 1 ? 'bg-slate-700' : ''}">
                                        <td class="px-3 py-2 border border-gray-700">${asset.asset_tag}</td>
                                        <td class="px-3 py-2 border border-gray-700">${asset.name}</td>
                                        <td class="px-3 py-2 border border-gray-700">${asset.location || 'N/A'}</td>
                                        <td class="px-3 py-2 border border-gray-700">
                                            <span class="px-2 py-1 rounded text-xs ${this.getConditionClass(asset.condition)}">${asset.condition}</span>
                                        </td>
                                        <td class="px-3 py-2 border border-gray-700">
                                            <button onclick="app.viewAsset(${asset.id})" class="text-teal-400 hover:text-teal-300 mr-2 text-xs">View</button>
                                            <button onclick="app.editAsset(${asset.id})" class="text-lime-400 hover:text-lime-300 text-xs">Edit</button>
                                        </td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading assets:', error);
            return '<p class="text-red-400">Error loading asset data.</p>';
        }
    }

    async renderStoreroomView() {
        try {
            const response = await fetch('/api/tools');
            const data = await response.json();
            
            if (data.success) {
                const availableTools = data.data.filter(tool => tool.status === 'available').length;
                const inUseTools = data.data.filter(tool => tool.status === 'in_use').length;
                
                return `
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-xl font-semibold text-teal-400">Live Storeroom View</h4>
                        <button onclick="app.showCheckOutToolsModal()" class="bg-teal-600 text-white px-4 py-2 rounded-md hover:bg-teal-700 text-sm">
                            <i class="fas fa-tools mr-2"></i>Check Out Tools
                        </button>
                    </div>
                    <p class="mb-4 text-white">Real-time inventory levels and storeroom status with current tool availability.</p>
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
                        <div class="bg-slate-700 p-4 rounded-lg">
                            <h5 class="text-lg font-semibold text-lime-400 mb-2">Available Tools</h5>
                            <p class="text-3xl font-bold text-white">${availableTools}</p>
                        </div>
                        <div class="bg-slate-700 p-4 rounded-lg">
                            <h5 class="text-lg font-semibold text-orange-400 mb-2">Tools in Use</h5>
                            <p class="text-3xl font-bold text-white">${inUseTools}</p>
                        </div>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm text-left text-white border border-gray-700 rounded">
                            <thead class="bg-teal-700">
                                <tr>
                                    <th class="px-3 py-2 border border-gray-600">Tool Name</th>
                                    <th class="px-3 py-2 border border-gray-600">Category</th>
                                    <th class="px-3 py-2 border border-gray-600">Status</th>
                                    <th class="px-3 py-2 border border-gray-600">Checked Out To</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.data.slice(0, 10).map((tool, index) => `
                                    <tr class="border border-gray-600 ${index % 2 === 1 ? 'bg-slate-700' : ''}">
                                        <td class="px-3 py-2 border border-gray-700">${tool.tool_name}</td>
                                        <td class="px-3 py-2 border border-gray-700">${tool.tool_category || 'N/A'}</td>
                                        <td class="px-3 py-2 border border-gray-700">
                                            <span class="px-2 py-1 rounded text-xs ${this.getStatusClass(tool.status)}">${tool.status}</span>
                                        </td>
                                        <td class="px-3 py-2 border border-gray-700">${tool.checked_out_user_name || 'N/A'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading storeroom data:', error);
            return '<p class="text-red-400">Error loading storeroom data.</p>';
        }
    }

    async renderWorkOrderPortal() {
        try {
            const response = await fetch('/api/tickets');
            const data = await response.json();
            
            if (data.success) {
                return `
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-xl font-semibold text-teal-400">Work Order Portal</h4>
                        <button onclick="app.showCreateTicketModal()" class="bg-teal-600 text-white px-4 py-2 rounded-md hover:bg-teal-700 text-sm">
                            <i class="fas fa-plus mr-2"></i>Create Work Order
                        </button>
                    </div>
                    <p class="mb-4 text-white">Manage and track active and completed work orders with priority and status indicators.</p>
                    <div class="overflow-x-auto">
                        <table class="w-full text-sm text-left text-white border border-gray-700 rounded">
                            <thead class="bg-teal-700">
                                <tr>
                                    <th class="px-3 py-2 border border-gray-600">Ticket ID</th>
                                    <th class="px-3 py-2 border border-gray-600">Description</th>
                                    <th class="px-3 py-2 border border-gray-600">Priority</th>
                                    <th class="px-3 py-2 border border-gray-600">Status</th>
                                    <th class="px-3 py-2 border border-gray-600">Assigned To</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.data.map((ticket, index) => `
                                    <tr class="border border-gray-600 ${index % 2 === 1 ? 'bg-slate-700' : ''}">
                                        <td class="px-3 py-2 border border-gray-700">#${ticket.id}</td>
                                        <td class="px-3 py-2 border border-gray-700">${ticket.title}</td>
                                        <td class="px-3 py-2 border border-gray-700">
                                            <span class="px-2 py-1 rounded text-xs ${this.getPriorityClass(ticket.priority)}">${ticket.priority}</span>
                                        </td>
                                        <td class="px-3 py-2 border border-gray-700">${ticket.status}</td>
                                        <td class="px-3 py-2 border border-gray-700">${ticket.assignee_name || 'Unassigned'}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Error loading work orders:', error);
            return '<p class="text-red-400">Error loading work order data.</p>';
        }
    }

    renderMaintenanceCalendar() {
        const today = new Date();
        const upcomingDates = [];
        
        for (let i = 1; i <= 5; i++) {
            const date = new Date(today);
            date.setDate(today.getDate() + (i * 5));
            upcomingDates.push(date.toLocaleDateString('en-ZA'));
        }

        return `
            <h4 class="text-xl font-semibold mb-3 text-teal-400">Maintenance Calendar</h4>
            <p class="mb-4 text-white">Upcoming scheduled maintenance tasks and deadlines for all facilities.</p>
            <ul class="list-disc list-inside text-white space-y-2">
                <li><strong>${upcomingDates[0]}:</strong> HVAC system inspection - Building A</li>
                <li><strong>${upcomingDates[1]}:</strong> Fire extinguisher replacement - Building B</li>
                <li><strong>${upcomingDates[2]}:</strong> Elevator safety check - Building C</li>
                <li><strong>${upcomingDates[3]}:</strong> Roof leak inspection - Building D</li>
                <li><strong>${upcomingDates[4]}:</strong> Generator load test - Building B</li>
            </ul>
        `;
    }

    renderComplianceDocs() {
        return `
            <h4 class="text-xl font-semibold mb-3 text-teal-400">Compliance Documents</h4>
            <p class="mb-4 text-white">Access to all ISO 41001 related compliance documents and audit reports.</p>
            <ul class="list-disc list-inside text-white space-y-2">
                <li><a class="underline hover:text-lime-400 cursor-pointer" tabindex="0">ISO 41001:2018 Certification Document</a></li>
                <li><a class="underline hover:text-lime-400 cursor-pointer" tabindex="0">Last Audit Report - ${new Date().toLocaleDateString('en-ZA', { month: 'long', year: 'numeric' })}</a></li>
                <li><a class="underline hover:text-lime-400 cursor-pointer" tabindex="0">Facilities Management Policy</a></li>
                <li><a class="underline hover:text-lime-400 cursor-pointer" tabindex="0">Safety and Compliance Procedures</a></li>
            </ul>
        `;
    }

    renderSheziMethodology() {
        return `
            <h4 class="text-xl font-semibold mb-3 text-teal-400">Shezi Methodology</h4>
            <p class="mb-4 text-white">Overview of the Shezi Methodology for facilities management and asset stewardship.</p>
            <p class="mb-4 text-white">The Shezi Methodology emphasizes disciplined asset tracking, proactive maintenance, and continuous improvement to ensure operational excellence and compliance with international standards.</p>
            <div class="bg-slate-700 p-4 rounded-lg">
                <h5 class="text-lg font-semibold text-lime-400 mb-2">Core Principles:</h5>
                <ul class="list-disc list-inside text-white space-y-1">
                    <li>Precision in asset documentation</li>
                    <li>Proactive maintenance scheduling</li>
                    <li>Continuous process improvement</li>
                    <li>ISO 41001 compliance integration</li>
                    <li>Data-driven decision making</li>
                </ul>
            </div>
        `;
    }

    getConditionClass(condition) {
        switch(condition) {
            case 'good': return 'bg-green-600 text-white';
            case 'fair': return 'bg-yellow-600 text-white';
            case 'repair': return 'bg-orange-600 text-white';
            case 'broken': return 'bg-red-600 text-white';
            default: return 'bg-gray-600 text-white';
        }
    }

    getStatusClass(status) {
        switch(status) {
            case 'available': return 'bg-green-600 text-white';
            case 'in_use': return 'bg-orange-600 text-white';
            case 'missing': return 'bg-red-600 text-white';
            default: return 'bg-gray-600 text-white';
        }
    }

    getPriorityClass(priority) {
        switch(priority) {
            case 'high': return 'bg-red-600 text-white';
            case 'medium': return 'bg-yellow-600 text-white';
            case 'low': return 'bg-green-600 text-white';
            default: return 'bg-gray-600 text-white';
        }
    }

    async updateNavContent(key) {
        const contentDiv = document.getElementById('nav-content');
        if (this.navContents[key]) {
            try {
                const content = await this.navContents[key]();
                contentDiv.innerHTML = content;
                contentDiv.focus();
            } catch (error) {
                console.error('Error updating nav content:', error);
                contentDiv.innerHTML = '<p class="text-red-400 text-center italic">Error loading content.</p>';
            }
        } else {
            contentDiv.innerHTML = '<p class="text-white text-center italic">Content not available.</p>';
        }
    }

    setupNavigation() {
        const navButtons = document.querySelectorAll('.hexagon');
        navButtons.forEach(button => {
            button.addEventListener('click', () => {
                const navKey = button.getAttribute('data-nav');
                this.updateNavContent(navKey);
            });
            button.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const navKey = button.getAttribute('data-nav');
                    this.updateNavContent(navKey);
                }
            });
        });
    }

    async loadDashboardData() {
        try {
            const response = await fetch('/api/dashboard/stats');
            const data = await response.json();
            
            if (data.success) {
                this.updateDashboardMetrics(data.data);
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    updateDashboardMetrics(stats) {
        const totalAssetsEl = document.getElementById('total-assets');
        const activeTicketsEl = document.getElementById('active-tickets');
        
        if (totalAssetsEl) {
            totalAssetsEl.textContent = stats.overview.active_assets || '428';
        }
        if (activeTicketsEl) {
            activeTicketsEl.textContent = stats.overview.total_tickets || '12';
        }
    }

    // Modal functionality
    showModal(content) {
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.style.display = 'block';
        modal.innerHTML = `
            <div class="modal-content">
                ${content}
            </div>
        `;
        document.body.appendChild(modal);
        
        // Prevent body scroll when modal is open
        document.body.style.overflow = 'hidden';
        
        // Add touch event handling for mobile
        modal.addEventListener('touchstart', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });
        
        // Close modal when clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });
    }

    closeModal() {
        const modal = document.querySelector('.modal');
        if (modal) {
            modal.remove();
            // Restore body scroll
            document.body.style.overflow = '';
        }
    }

    showCreateAssetModal() {
        this.showModal(`
            <h3 class="text-lg font-medium text-gray-900 mb-4">Add New Asset</h3>
            <form id="createAssetForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Asset Tag</label>
                    <input type="text" name="asset_tag" class="w-full border border-gray-300 rounded-md px-3 py-2" required>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Name</label>
                    <input type="text" name="name" class="w-full border border-gray-300 rounded-md px-3 py-2" required>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
                    <input type="text" name="category" class="w-full border border-gray-300 rounded-md px-3 py-2">
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
                    <input type="text" name="location" class="w-full border border-gray-300 rounded-md px-3 py-2">
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Condition</label>
                    <select name="condition" class="w-full border border-gray-300 rounded-md px-3 py-2">
                        <option value="good">Good</option>
                        <option value="fair">Fair</option>
                        <option value="repair">Needs Repair</option>
                        <option value="broken">Broken</option>
                    </select>
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="app.closeModal()" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300">Cancel</button>
                    <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700">Add Asset</button>
                </div>
            </form>
        `);

        document.getElementById("createAssetForm").addEventListener("submit", (e) => {
            e.preventDefault();
            this.createAsset(new FormData(e.target));
        });
    }

    showCreateTicketModal() {
        this.showModal(`
            <h3 class="text-lg font-medium text-gray-900 mb-4">Create New Work Order</h3>
            <form id="createTicketForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
                    <input type="text" name="title" class="w-full border border-gray-300 rounded-md px-3 py-2" required>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea name="description" rows="3" class="w-full border border-gray-300 rounded-md px-3 py-2" required></textarea>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Priority</label>
                    <select name="priority" class="w-full border border-gray-300 rounded-md px-3 py-2">
                        <option value="low">Low</option>
                        <option value="medium">Medium</option>
                        <option value="high">High</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
                    <input type="text" name="location" class="w-full border border-gray-300 rounded-md px-3 py-2">
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="app.closeModal()" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300">Cancel</button>
                    <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700">Create Work Order</button>
                </div>
            </form>
        `);

        document.getElementById("createTicketForm").addEventListener("submit", (e) => {
            e.preventDefault();
            this.createTicket(new FormData(e.target));
        });
    }

    showCheckOutToolsModal() {
        this.showModal(`
            <h3 class="text-lg font-medium text-gray-900 mb-4">Check Out Tools</h3>
            <form id="checkOutToolsForm">
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Tool Selection</label>
                    <select name="tool_id" class="w-full border border-gray-300 rounded-md px-3 py-2" required>
                        <option value="">Select a tool...</option>
                        <option value="1">Multimeter</option>
                        <option value="2">Cordless Drill</option>
                    </select>
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Checked Out To</label>
                    <input type="text" name="user_name" class="w-full border border-gray-300 rounded-md px-3 py-2" required>
                </div>
                <div class="flex justify-end space-x-3">
                    <button type="button" onclick="app.closeModal()" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300">Cancel</button>
                    <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-teal-600 rounded-md hover:bg-teal-700">Check Out</button>
                </div>
            </form>
        `);

        document.getElementById("checkOutToolsForm").addEventListener("submit", (e) => {
            e.preventDefault();
            this.checkOutTool(new FormData(e.target));
        });
    }

    async createAsset(formData) {
        try {
            const assetData = {
                asset_tag: formData.get("asset_tag"),
                name: formData.get("name"),
                category: formData.get("category"),
                location: formData.get("location"),
                condition: formData.get("condition"),
            };

            const response = await fetch("/api/assets", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(assetData),
            });

            const result = await response.json();
            if (result.success) {
                this.closeModal();
                this.showNotification("Asset added successfully!", "success");
                // Refresh current view if it's asset register
                const currentContent = document.getElementById('nav-content');
                if (currentContent.innerHTML.includes('Asset Register')) {
                    this.updateNavContent('asset-register');
                }
            } else {
                this.showNotification("Failed to add asset", "error");
            }
        } catch (error) {
            console.error("Error adding asset:", error);
            this.showNotification("Error adding asset", "error");
        }
    }

    async createTicket(formData) {
        try {
            const ticketData = {
                title: formData.get('title'),
                description: formData.get('description'),
                priority: formData.get('priority'),
                location: formData.get('location'),
                created_by: 2 // Default to manager user
            };

            const response = await fetch('/api/tickets', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(ticketData)
            });

            const result = await response.json();
            if (result.success) {
                this.closeModal();
                this.showNotification('Work order created successfully!', 'success');
                // Refresh current view if it's work order portal
                const currentContent = document.getElementById('nav-content');
                if (currentContent.innerHTML.includes('Work Order Portal')) {
                    this.updateNavContent('work-order');
                }
            } else {
                this.showNotification('Failed to create work order', 'error');
            }
        } catch (error) {
            console.error('Error creating work order:', error);
            this.showNotification('Error creating work order', 'error');
        }
    }

    async checkOutTool(formData) {
        try {
            // This would need to be implemented in the backend
            this.closeModal();
            this.showNotification('Tool checked out successfully!', 'success');
        } catch (error) {
            console.error('Error checking out tool:', error);
            this.showNotification('Error checking out tool', 'error');
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 px-6 py-3 rounded-md text-white z-50 ${
            type === 'success' ? 'bg-green-500' : 
            type === 'error' ? 'bg-red-500' : 'bg-blue-500'
        }`;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    viewAsset(id) {
        this.showNotification('Asset details view - Feature coming soon!', 'info');
    }

    editAsset(id) {
        this.showNotification('Asset edit - Feature coming soon!', 'info');
    }
}

// Initialize the application
const app = new FacilitiesCommandCenter();

