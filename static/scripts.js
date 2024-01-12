// Filtering by status
var logs = Array.from(document.getElementsByClassName('log'));
function showOnly(className) {
    var filteredLogs = [];
    if (className === 'all') {
        filteredLogs = logs;
    } else {
        filteredLogs = logs.filter(log => log.classList.contains(className));
    }
    var logContainer = document.getElementById('log-container');
    logContainer.innerHTML = '';
    filteredLogs.forEach(log => {
        var clone = log.cloneNode(true);
        logContainer.appendChild(clone);
    });
}

// Copy start and end times for the line
function copyTime() {
    var selection = window.getSelection();
    var range = document.createRange();

    var clickedSpan = selection.anchorNode.parentElement;

    var textToCopy = clickedSpan.textContent.trim();
    var startIndex = textToCopy.indexOf('Start');
    var text = textToCopy.substring(startIndex);

    var tempTextArea = document.createElement('textarea');
    tempTextArea.value = text;

    document.body.appendChild(tempTextArea);

    range.selectNodeContents(tempTextArea);
    selection.removeAllRanges();
    selection.addRange(range);
    tempTextArea.select();
    document.execCommand('copy');

    document.body.removeChild(tempTextArea);
}

// Searching
// Enter key is 13, Esc key is 27, Enter filters, Esc clears filter
function handleSearch(event) {
    if (!event || event.keyCode === 13) {
        searchContent();
        event.preventDefault();
    } else if (event.keyCode === 27) {
        clearFilter();
        event.preventDefault();
    }
}

// Filtering by content
function searchContent() {
    var searchInput = document.querySelector('.form-control');
    var query = searchInput.value.trim().toLowerCase();

    var searchableElements = document.querySelectorAll('.log');

    for (var i = 0; i < searchableElements.length; i++) {
        var element = searchableElements[i];
        var content = element.textContent.toLowerCase();

        if (content.includes(query)) {
            element.style.display = 'block';
        } else {
            element.style.display = 'none';
        }
    }
}

// Clearing filter
function clearFilter() {
    var searchInput = document.querySelector('.form-control');
    searchInput.value = '';

    var hiddenElements = document.querySelectorAll('.log[style="display: none;"]');
    hiddenElements.forEach(function (element) {
        element.style.display = 'block';
    });
}