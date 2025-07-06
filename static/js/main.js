// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // --- Calculator Page Logic ---
    const calculatorForm = document.getElementById('calculator-form');
    if (calculatorForm) {
        const serviceSelect = document.getElementById('service');
        const planSelect = document.getElementById('plan');

        serviceSelect.addEventListener('change', function() {
            const serviceId = this.value;
            planSelect.disabled = true;
            planSelect.innerHTML = '<option>Loading plans...</option>';
            if (!serviceId) return;

            fetch(`/api/get-plans/${serviceId}/`)
                .then(response => response.json())
                .then(data => {
                    planSelect.innerHTML = '<option value="" selected disabled>Choose a plan...</option>';
                    if (data.length > 0) {
                        data.forEach(plan => {
                            const option = document.createElement('option');
                            option.value = plan.id; // Use plan ID now
                            option.textContent = `${plan.plan_name} (${plan.country}) - ${plan.price} ${plan.currency}`;
                            planSelect.appendChild(option);
                        });
                        planSelect.disabled = false;
                    } else {
                        planSelect.innerHTML = '<option>No plans found for this region</option>';
                    }
                });
        });
    }

    // --- Dashboard Page Logic ---
     const dashboard = document.getElementById('category-chart');
    if (dashboard) {
        let userProfile = JSON.parse(document.getElementById('user-profile-json').textContent);
        let subscriptions = JSON.parse(document.getElementById('user-subscriptions-json').textContent);
        let categoryChart;

        const totalCostEl = document.getElementById('total-cost');
        const totalTimeCostEl = document.getElementById('total-time-cost');
        const subscriptionListEl = document.getElementById('subscription-list');
        const emptyStatePanel = document.getElementById('empty-state-panel');
        const addSubForm = document.getElementById('calculator-form');
        const addFirstSubBtn = document.getElementById('add-first-sub-btn');
        const addSubSection = document.getElementById('add-subscription-section');
        const chartOverlay = document.getElementById('chart-overlay');


        function formatTime(totalMinutes) {
            if (totalMinutes <= 0) return '--';
            const hoursPart = Math.floor(totalMinutes / 60);
            const minutesPart = Math.round(totalMinutes % 60);
            let result = '';
            if (hoursPart > 0) result += `${hoursPart} hr${hoursPart > 1 ? 's' : ''} `;
            if (minutesPart > 0) result += `${minutesPart} min${minutesPart > 1 ? 's' : ''}`;
            return result.trim() || 'Less than a minute';
        }

        function calculateTimeCost(price) {
            if (!userProfile || userProfile.income <= 0 || userProfile.hours <= 0) return 0;
            const hourlyWage = (userProfile.income / 4.33) / userProfile.hours;
            return (price / hourlyWage) * 60; // Return in minutes
        }

        function renderSubscriptionList() {
            subscriptionListEl.innerHTML = ''; // Clear list
            if (subscriptions.length === 0) {
                emptyStatePanel.classList.remove('hidden');
                subscriptionListEl.classList.add('hidden');
                chartOverlay.classList.remove('hidden');
            } else {
                emptyStatePanel.classList.add('hidden');
                subscriptionListEl.classList.remove('hidden');
                chartOverlay.classList.add('hidden');

                subscriptions.forEach(sub => {
                    const li = document.createElement('li');
                    li.className = 'flex items-center justify-between py-4';
                    li.innerHTML = `
                        <div class="flex items-center space-x-4">
                            <div>
                                <p class="text-sm font-medium text-gray-900">${sub.service_name}</p>
                                <p class="text-sm text-gray-500">${sub.plan_name}</p>
                            </div>
                        </div>
                        <div class="text-right">
                            <p class="text-sm font-medium text-gray-900">$${sub.price.toFixed(2)}</p>
                            <button data-id="${sub.id}" class="remove-btn text-xs text-red-500 hover:text-red-700">Remove</button>
                        </div>
                    `;
                    subscriptionListEl.appendChild(li);
                });
            }
        }

        function updateDashboard() {
            const totalCost = subscriptions.reduce((acc, sub) => acc + sub.price, 0);
            const totalTimeInMinutes = calculateTimeCost(totalCost);

            totalCostEl.textContent = totalCost.toFixed(2);
            totalTimeCostEl.textContent = formatTime(totalTimeInMinutes);

            const categoryData = subscriptions.reduce((acc, sub) => {
                acc[sub.category] = (acc[sub.category] || 0) + sub.price;
                return acc;
            }, {});

            const labels = Object.keys(categoryData);
            const data = Object.values(categoryData);

            if (categoryChart) {
                categoryChart.data.labels = labels;
                categoryChart.data.datasets[0].data = data;
                categoryChart.update();
            }
        }

        function initializeChart() {
            const ctx = document.getElementById('category-chart').getContext('2d');
            categoryChart = new Chart(ctx, {
                type: 'doughnut',
                data: { labels: [], datasets: [{ data: [], backgroundColor: ['#4f46e5', '#7c3aed', '#db2777', '#f59e0b', '#10b981', '#3b82f6'] }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }
            });
        }

        // --- Event Listeners ---

        addFirstSubBtn.addEventListener('click', () => {
            addSubSection.scrollIntoView({ behavior: 'smooth' });
        });

        addSubForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const planId = document.getElementById('plan').value;
            if (!planId) return;

            fetch('/api/add-subscription/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value },
                body: JSON.stringify({ plan_id: planId })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success') {
                    subscriptions.push(data.subscription);
                    renderSubscriptionList();
                    updateDashboard();
                    addSubForm.reset();
                    document.getElementById('plan').innerHTML = '<option value="" selected disabled>Select a service first</option>';
                    document.getElementById('plan').disabled = true;
                } else { alert(data.message); }
            });
        });

        subscriptionListEl.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-btn')) {
                const subId = e.target.dataset.id;
                if (!confirm('Are you sure?')) return;

                fetch(`/api/remove-subscription/${subId}/`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.status === 'success') {
                            subscriptions = subscriptions.filter(s => s.id != subId);
                            renderSubscriptionList();
                            updateDashboard();
                        } else { alert(data.message); }
                    });
            }
        });

        // Initial setup
        initializeChart();
        renderSubscriptionList();
        updateDashboard();
    }
});