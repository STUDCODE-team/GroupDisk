// Получаем все элементы меню
const navItems = document.querySelectorAll('.nav-item');
const dropArea = document.querySelector('.drop-section')

const fileSelector = document.querySelector('.upload-button')
const fileSelectorInput = document.getElementById('fileSelectorInput');

const documentsArea = document.querySelector('.documents');


let isDragging = false; // Флаг для отслеживания состояния перетаскивания

document.addEventListener('DOMContentLoaded', () => {
    getFiles();
})

function getFiles(parentId = null) {
    fetch('/api/get_userfiles', {
        method: 'POST',
        body: {}
    }).then(response => response.text())
        .then(files => init(JSON.parse(files)));
}

function init(files) {
    documentsArea.innerHTML = '';

    for (let file of files) {
        console.warn(file)
        if (file.ext !== "...") {
            documentsArea.insertAdjacentHTML('beforeend', `
                <div class="file-object">
                    <div class="file-icon">
                        <div class="file-corner"></div>
                        <div class="file-extension">${file.extension}</div>
                    </div>
                    <div class="file-name">${file.name}</div> <!-- Переместили название файла сюда -->
                </div>
                
            `);
        } else {
            documentsArea.insertAdjacentHTML('beforeend', `
                <div class="file-object">
                <img src="../static/folder.png" alt="Folder Icon" class="folder-icon"> 
                <div class="file-name">${file.name}</div>
                </div>
                
            `);
        }

    }
}



// Добавляем событие клика на каждый пункт меню
navItems.forEach(item => {
    item.addEventListener('click', function() {
        document.querySelector('.nav-item-active').classList.remove('nav-item-active');
        if (!this.classList.contains('nav-item-logout'))
            this.classList.add('nav-item-active');
    });
});


// Показать область сброса при перетаскивании
document.addEventListener('dragover', (event) => {
    event.preventDefault(); // Предотвращаем действие по умолчанию
    if (!isDragging) {
        dropArea.classList.add('drag-over'); // Показываем область сброса
        isDragging = true; // Устанавливаем флаг
    }
});

// Показать область сброса, когда перетаскиваемый элемент входит в неё
dropArea.addEventListener('dragenter', (event) => {
    event.preventDefault(); // Предотвращаем действие по умолчанию
    if (!isDragging) {
        dropArea.classList.add('drag-over'); // Показываем область сброса
        isDragging = true; // Устанавливаем флаг
    }
});

// Скрыть область сброса, когда перетаскиваемый элемент покидает рабочую область
dropArea.addEventListener('dragleave', (event) => {
    // Проверяем, если указатель действительно покинул область
    if (!dropArea.contains(event.relatedTarget)) {
        dropArea.classList.remove('drag-over'); // Скрываем область сброса
        isDragging = false; // Сбрасываем флаг
    }
});


// Handle drop event
dropArea.addEventListener('drop', async (event) => {
    event.preventDefault();
    dropArea.classList.remove('drag-over');
    isDragging = false;

    uploadFiles(event.dataTransfer.files);
});


fileSelector.onclick = () => fileSelectorInput.click()
fileSelectorInput.onchange = () => {
    uploadFiles(fileSelectorInput.files)
}


function uploadFiles(files) {
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]); // используем 'files' как ключ
    }

    // сделать отдельной функцией
    fetch('/api/upload_userfiles', {
        method: 'POST',
        body: formData
    }).then(response => response.text())
      .then(data => getFiles());
}
