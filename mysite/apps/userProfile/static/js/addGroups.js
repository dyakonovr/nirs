const userID = Number(document.querySelector('[data-user-id]').innerHTML);
const groupList = document.querySelector('#group-list');
const groupBtn = document.querySelector('#group-btn');
const groupInput = document.querySelector('#group-input');
const groupEmpty = document.querySelector('#group-empty');
const studentsEmpty = document.querySelector('#students-empty');
const studentsList = document.querySelector('#students-list');

function getToken() {
  function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  return getCookie('csrftoken');
}



document.addEventListener('DOMContentLoaded', function () {
  groupBtn.addEventListener('click', () => {
    const inputValue = groupInput.value;
    if (!document.querySelector(`[data-group="${inputValue}"]`)) {
      console.log(inputValue, userID);
      axios.post('/api/createGroup/', {
        "user": userID,
        "group": inputValue
      }, {
        headers: {
          "X-CSRFToken": getToken()
        }
      })
        .then(function () {
          groupList.innerHTML += `
            <li class="accordion" data-group="${inputValue}">
                <div class="d-flex align-items-center accordion__control" aria-expanded="false" onclick="accordionOpen(event)">
                    <button class="accordion__btn">
                        <span class="accordion__title">${inputValue}</span>
                    </button>
                    <button class="ms-auto btn btn-sm btn-danger" onclick="deleteGroup(event)">Удалить группу</button>
                </div>
                <ol class="accordion__content" aria-hidden="true" id="students-list">
                    <span class="fs-5 visually-hidden" id="students-empty">Пока здесь нет студенов...</span>
                    <li class="fs-5 mb-2">Ученик 1 <button class="btn btn-sm btn-warning ms-2" style="margin-top: -3px;" id="group-student-delete" onclick="deleteStudent(event)">Удалить</button></li>
                    <li class="fs-5 mb-2">Ученик 2 <button class="btn btn-sm btn-warning ms-2" style="margin-top: -3px;" id="group-student-delete" onclick="deleteStudent(event)">Удалить</button></li>
                    <li class="fs-5 mb-2">Ученик 3 <button class="btn btn-sm btn-warning ms-2" style="margin-top: -3px;" id="group-student-delete" onclick="deleteStudent(event)">Удалить</button></li>
                </ol>
            </li>
          `;
        })
        .catch(function (error) {
          console.error(error);
          alert('Произошла ошибка. Попробуйте еще раз!')
        });
      
    } else alert('Такая группа уже существует!');

    groupInput.value = '';
  });
});

function deleteStudent(e) {
  const currentParent = e.currentTarget.parentElement;
  currentParent.remove();

  if (studentsList.children.length - 1 === 0) studentsEmpty.classList.remove('visually-hidden');
}

function deleteGroup(e) {
  const currentParent = e.currentTarget.parentElement.parentElement;
  currentParent.remove();

  if (groupList.children.length - 1 === 0) groupEmpty.classList.remove('visually-hidden');
}