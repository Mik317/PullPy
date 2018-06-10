function total(num){
	var ctx = document.getElementById("total").getContext('2d');
	var chart = new Chart(ctx, {
	    type: 'doughnut',
	    data: {
	        labels: ['Total Bots'],
	        datasets: [{
	            label: 'Total Bots',
	            data: [num],
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)'
	            ],
	            borderWidth: 1
	        }]
	    }
	});	
}


function os(win, nix) {
	var ctx2 = document.getElementById("os").getContext('2d');
	var chart2 = new Chart(ctx2, {
	    type: 'doughnut',
	    data: {
	        labels: ["Win", "Unix"],
	        datasets: [{
	            label: "Bots' Os",
	            data: [win, nix],
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)'
	            ],
	            borderWidth: 1
	        }]
	    }
	});
}