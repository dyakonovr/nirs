const userID = Number(document.querySelector('[data-user-id]').innerHTML);
const groupList = document.querySelector('#group-list');
const groupBtn = document.querySelector('#group-btn');
const groupInput = document.querySelector('#group-input');
const groupEmpty = document.querySelector('#group-empty');
const token = getToken();

console.log(groupEmpty);

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
  function makeCode(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
      counter += 1;
    }
    return result;
  }

  groupBtn.addEventListener('click', () => {
    const inputValue = groupInput.value;
    if (!document.querySelector(`[data-group="${inputValue}"]`)) {
      axios.post('/api/createGroup/', {
        "user": userID,
        "group": inputValue,
        "code": makeCode(51),
      }, {
        headers: {
          "X-CSRFToken": token
        }
      })
        .then(function (response) {
          const groupID = response.data.id;
          const groupCode = response.data.code;
          const domain = document.domain;

          groupList.innerHTML += `
            <li class="group-item mt-3" data-group="${inputValue}" data-group-id="${groupID}">
              <div class="d-flex align-items-center">
                  <h3>${inputValue}</h3>
                  <button class="btn btn-info ms-2 btn-sm text-light" onclick="copyLink(event)" data-link="${domain}:8000/addGroup?user_id=${userID}&group_id=${groupID}&code=${groupCode}">Скопировать ссылку на группу</button>
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
  const currentStudentList = currentParent.parentNode;
  const currentStudentsEmpty = currentStudentList.querySelector('#students-empty');
  console.log(currentStudentsEmpty);
  const studentID = Number(currentParent.getAttribute("data-student-id"));
  let userToken;
  axios.get(`/api/getToken/${studentID}/`, {}).then(function (response) {
    userToken = response.data.key
    axios.delete(`/api/deleteStudent/${studentID}/`, {
      headers: {
        "Authorization": `Token ${userToken}`,
      }
    }).then(function () {
      currentParent.remove();
      if (currentStudentList.children.length - 1 === 0) currentStudentsEmpty.classList.remove('visually-hidden');
    }).catch(function (error) {
      console.error(error);
      alert("Произошла ошибка! Попробуйте ещё раз.");
    })
  }).catch(function (error) {
    console.error(error);
    alert("Произошла ошибка! Попробуйте ещё раз.");
  })
  
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

const notification_link = document.querySelector('#notification_link');

function copyLink(e) {
  const link = e.currentTarget.getAttribute("data-link");

  notification_link.classList.add('notification--active');
  navigator.clipboard.writeText(link);

  setTimeout(function () { notification_link.classList.remove('notification--active') }, 3000);
}