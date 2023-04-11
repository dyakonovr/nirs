const userID = Number(document.querySelector('[data-user-id]').innerHTML);
const groupList = document.querySelector('#group-list');
const groupBtn = document.querySelector('#group-btn');
const groupInput = document.querySelector('#group-input');
const groupEmpty = document.querySelector('#group-empty');
// const studentsEmpty = document.querySelector('#students-empty');
// const studentsList = document.querySelector('#students-list');
const token = getToken();

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
      axios.post('/api/createGroup/', {
        "user": userID,
        "group": inputValue
      }, {
        headers: {
          "X-CSRFToken": token
        }
      })
        .then(function (response) {
          const groupID = response.data.id;
          groupList.innerHTML += `
            <li class="group-item" data-group="${inputValue}" data-group-id="${groupID}">
              <div class="d-flex align-items-center">
                  <h3>${inputValue}</h3>
                  <button class="ms-2 btn btn-sm btn-danger" onclick="deleteGroup(event)">Удалить
                      группу</button>
              </div>
              <span class="fs-5" id="students-empty">Эта группа пуста!</span>
          </li>
          `;

          if (groupList.children.length - 1 === 0) groupList.classList.remove('visually-hidden');

          groupEmpty.classList.add('visually-hidden');
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
  const currentParent = e.currentTarget.parentElement.parentNode;
  console.log(currentParent);
  const currentStudentList = currentParent.parentNode;
  console.log(currentStudentList);
  const currentStudentsEmpty = currentStudentList.querySelector('#students-empty');

  currentParent.remove();
  console.log(currentStudentList.children.length - 1);
  if (currentStudentList.children.length - 1 === 0) currentStudentsEmpty.classList.remove('visually-hidden');
}

function deleteGroup(e) {
  const groupParent = e.currentTarget.parentElement.parentElement;
  const groupID = groupParent.getAttribute("data-group-id");

  axios.delete(`/api/deleteGroup/${groupID}/`, {
    headers: {
      "X-CSRFToken": token
    }
  })
    .then(function () {
      groupParent.remove();
      if (groupList.children.length === 0) setTimeout(groupEmpty.classList.remove('visually-hidden'), 500);
    })
    .catch(function (error) {
      console.error(error);
      alert('Произошла ошибка. Попробуйте еще раз!')
    });
}