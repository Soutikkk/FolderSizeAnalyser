document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const pathInput = document.getElementById('pathInput');
    const loader = document.getElementById('loader');
    const results = document.getElementById('results');
    const errorMsg = document.getElementById('errorMsg');
    const errorText = document.getElementById('errorText');
    const loadingPath = document.getElementById('loadingPath');

    let currentChart = null;

    analyzeBtn.addEventListener('click', () => {
        const path = pathInput.value.trim();
        if (!path) return;

        // Reset UI
        results.classList.add('hidden');
        errorMsg.classList.add('hidden');
        loader.classList.remove('hidden');
        loadingPath.textContent = path;

        fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ path: path })
        })
        .then(res => res.json())
        .then(data => {
            loader.classList.add('hidden');
            
            if (data.success) {
                renderResults(data);
                results.classList.remove('hidden');
            } else {
                showError(data.error || 'An error occurred during analysis.');
            }
        })
        .catch(err => {
            loader.classList.add('hidden');
            showError('Failed to connect to the server. Make sure it is running.');
            console.error(err);
        });
    });

    function showError(msg) {
        errorText.textContent = msg;
        errorMsg.classList.remove('hidden');
    }

    function formatBytes(bytes, decimals = 2) {
        if (!+bytes) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
    }

    function renderResults(data) {
        // Summary Cards
        document.getElementById('totalSizeResult').textContent = formatBytes(data.total_size);
        document.getElementById('totalItemsResult').textContent = data.children.length;

        // Render Chart
        renderChart(data.file_types);

        // Render Children List
        const childrenList = document.getElementById('childrenList');
        childrenList.innerHTML = '';
        if (data.children.length === 0) {
            childrenList.innerHTML = '<li class="file-item"><div class="file-info">Empty Directory</div></li>';
        } else {
            data.children.forEach(child => {
                const li = document.createElement('li');
                li.className = 'file-item';
                
                const iconClass = child.is_dir ? 'fa-solid fa-folder' : 'fa-solid fa-file';
                
                li.innerHTML = `
                    <div class="file-info">
                        <i class="${iconClass}"></i>
                        <span class="file-name" title="${child.name}">${child.name}</span>
                    </div>
                    <div class="file-size">${formatBytes(child.size)}</div>
                `;
                childrenList.appendChild(li);
            });
        }

        // Render Largest Files Table
        const largestFilesBody = document.getElementById('largestFilesBody');
        largestFilesBody.innerHTML = '';
        if (data.largest_files.length === 0) {
            largestFilesBody.innerHTML = '<tr><td colspan="3" style="text-align:center;">No files found</td></tr>';
        } else {
            data.largest_files.forEach(file => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>
                        <div class="file-info">
                            <i class="fa-solid fa-file"></i>
                            <span class="file-name" title="${file.name}">${file.name}</span>
                        </div>
                    </td>
                    <td><span class="path-text" title="${file.path}">${file.path}</span></td>
                    <td>${formatBytes(file.size)}</td>
                `;
                largestFilesBody.appendChild(tr);
            });
        }
    }

    function renderChart(fileTypes) {
        const ctx = document.getElementById('fileTypeChart').getContext('2d');
        
        if (currentChart) {
            currentChart.destroy();
        }

        // Sort by size and get top 8, group rest into "Others"
        const sortedTypes = Object.entries(fileTypes).sort((a, b) => b[1] - a[1]);
        
        let labels = [];
        let data = [];
        const topLimit = 8;
        
        let otherSize = 0;
        
        sortedTypes.forEach((item, index) => {
            if (index < topLimit) {
                labels.push(item[0] === 'unknown' ? 'No Ext' : item[0]);
                data.push(item[1]);
            } else {
                otherSize += item[1];
            }
        });
        
        if (otherSize > 0) {
            labels.push('Others');
            data.push(otherSize);
        }

        if (data.length === 0) {
            labels = ['Empty'];
            data = [1];
        }

        const colors = [
            '#3b82f6', '#8b5cf6', '#ec4899', '#10b981', '#f59e0b',
            '#ef4444', '#06b6d4', '#6366f1', '#64748b'
        ];

        currentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 0,
                    hoverOffset: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '70%',
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            color: '#94a3b8',
                            font: { family: 'Inter', size: 12 },
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.raw !== null) {
                                    // Make sure "Empty" chart displays correctly without bytes if it's fake data
                                    if(context.label === 'Empty' && context.raw === 1) {
                                        return '0 Bytes';
                                    }
                                    label += formatBytes(context.raw);
                                }
                                return label;
                            }
                        },
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleFont: { family: 'Inter', size: 13 },
                        bodyFont: { family: 'Inter', size: 13 },
                        padding: 12,
                        cornerRadius: 8,
                        displayColors: true
                    }
                }
            }
        });
    }

    // Allow Enter key to trigger analysis
    pathInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            analyzeBtn.click();
        }
    });

});
