// Получаем все элементы меню
const navItems = document.querySelectorAll('.nav-item');
const dropArea = document.querySelector('.drop-section')

let isDragging = false; // Флаг для отслеживания состояния перетаскивания


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
    isDragging = false; // Сбрасываем флаг

    const files = event.dataTransfer.files;
    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]); // используем 'files' как ключ
    }

    // сделать отдельной функцией
    fetch('/api/upload_userfiles', {
        method: 'POST',
        body: formData
    }).then(response => response.text())
      .then(data => console.log(data));

});



// upload files with browse button
// fileSelector.onclick = () => fileSelectorInput.click()
// fileSelectorInput.onchange = () => {
//     [...fileSelectorInput.files].forEach((file) => {
//         if(typeValidation(file.type)){
//             uploadFile(file)
//         }
//     })
// }

// // when file is over the drag area
// dropArea.ondragover = (e) => {
//     e.preventDefault();
//     [...e.dataTransfer.items].forEach((item) => {
//         if(typeValidation(item.type)){
//             dropArea.classList.add('drag-over-effect')
//         }
//     })
// }
// // when file leave the drag area
// dropArea.ondragleave = () => {
//     dropArea.classList.remove('drag-over-effect')
// }
// // when file drop on the drag area
// dropArea.ondrop = (e) => {
//     e.preventDefault();
//     dropArea.classList.remove('drag-over-effect')
//     if(e.dataTransfer.items){
//         [...e.dataTransfer.items].forEach((item) => {
//             if(item.kind === 'file'){
//                 const file = item.getAsFile();
//                 if(typeValidation(file.type)){
//                     uploadFile(file)
//                 }
//             }
//         })
//     }else{
//         [...e.dataTransfer.files].forEach((file) => {
//             if(typeValidation(file.type)){
//                 uploadFile(file)
//             }
//         })
//     }
// }


// // check the file type
// function typeValidation(type){
//     var splitType = type.split('/')[0]
//     if( type == 'application/pdf' ||
//         splitType == 'image' ||
//         splitType == 'video')
//     {
//         return true
//     }
// }

// // upload file function
// function uploadFile(file){
//     listSection.style.display = 'block'
//     var li = document.createElement('li')
//     li.classList.add('in-prog')
//     listContainer.prepend(li)
//     var http = new XMLHttpRequest()
//     var data = new FormData()
//     data.append('file', file)
//     http.onload = () => {
//         li.classList.add('complete')
//         li.classList.remove('in-prog')
//     }
//     http.upload.onprogress = (e) => {
//         var percent_complete = (e.loaded / e.total)*100
//         li.querySelectorAll('span')[0].innerHTML = Math.round(percent_complete) + '%'
//         li.querySelectorAll('span')[1].style.width = percent_complete + '%'
//     }
//     http.open('POST', 'sender.php', true)
//     http.send(data)
//     li.querySelector('.cross').onclick = () => http.abort()
//     http.onabort = () => li.remove()
//     console.log("XXX")
// }
// // find icon for file
// function iconSelector(type){
//     var splitType = (type.split('/')[0] == 'application') ? type.split('/')[1] : type.split('/')[0];
//     return splitType + '.png'
// }