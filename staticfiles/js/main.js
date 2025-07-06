// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    const serviceSelect = document.getElementById('service');
    const planSelect = document.getElementById('plan');
    const calculatorForm = document.getElementById('calculator-form');
    const resultsDiv = document.getElementById('results');
    const resultText = document.getElementById('result-text');

    if (serviceSelect) {
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
                            option.value = plan.price; // We only need the price for calculation
                            option.textContent = `${plan.plan_name} (${plan.country}) - ${plan.price} ${plan.currency}`;
                            planSelect.appendChild(option);
                        });
                        planSelect.disabled = false;
                    } else {
                        planSelect.innerHTML = '<option>No plans found for this region</option>';
                    }
                })
                .catch(error => {
                    console.error('Error fetching plans:', error);
                    planSelect.innerHTML = '<option>Error loading plans</option>';
                });
        });
    }

    if (calculatorForm) {
        calculatorForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const income = parseFloat(document.getElementById('income').value);
            const hours = parseFloat(document.getElementById('hours').value);
            const planPrice = parseFloat(planSelect.value);

            if (isNaN(income) || isNaN(hours) || isNaN(planPrice) || income <= 0 || hours <= 0) {
                alert('Please enter valid income, hours, and select a plan.');
                return;
            }

            // Calculation
            const weeklyIncome = income / 4.33;
            const hourlyWage = weeklyIncome / hours;
            const timeCostHours = planPrice / hourlyWage;

            // Format the result
            const totalMinutes = timeCostHours * 60;
            const hoursPart = Math.floor(totalMinutes / 60);
            const minutesPart = Math.round(totalMinutes % 60);

            let formattedResult = '';
            if (hoursPart > 0) {
                formattedResult += `${hoursPart} hour${hoursPart > 1 ? 's' : ''}`;
            }
            if (minutesPart > 0) {
                if (hoursPart > 0) formattedResult += ' and ';
                formattedResult += `${minutesPart} minute${minutesPart > 1 ? 's' : ''}`;
            }
            if (formattedResult === '') {
                formattedResult = 'Less than a minute';
            }

            resultText.textContent = formattedResult;
            resultsDiv.classList.remove('hidden');
        });
    }
});
