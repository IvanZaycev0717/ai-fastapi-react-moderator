import { useEffect, useState } from "react";
import "./App.css";
import { Modal } from "@mui/material";

const BASE_URL = "http://127.0.0.1:8000/comments/";

function App() {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [username, setUsername] = useState("");
  const [commentId, setCommentId] = useState(0);
  const [openCreateComment, setOpenCreateComment] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(BASE_URL)
      .then((response) => {
        if (response.status === 204) {
          return null;
        }
        return response.json();
      })
      .then((data) => {
        if (data === null) {
          setMessage("Ещё нет ни одного комментария");
        } else {
          setComments(data);
        }
      })
      .catch((error) => console.log(error));
  }, []);

  const publishComment = (event) => {
    event?.preventDefault();
    const json_string = JSON.stringify({
      username,
      original_text: newComment,
    });

    if (commentId === 0) {
      const requestOptions = {
        method: "POST",
        headers: new Headers({ "Content-Type": "application/json" }),
        body: json_string,
      };
      fetch(BASE_URL, requestOptions)
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then(() => fetchComments())
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          setNewComment("");
          setUsername("");
          setOpenCreateComment(false);
          setMessage("");
        });
    } else {
      fetch(BASE_URL + `${commentId}/edit/${newComment}`, { method: "PUT" })
        .then((response) => {
          if (response.ok) {
            return response.json();
          }
        })
        .then(() => fetchComments())
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          setNewComment("");
          setUsername("");
          setCommentId(0);
          setOpenCreateComment(false);
        });
    }
  };

  const handleDeleteComment = (comment_id) => {
    fetch(BASE_URL + comment_id, { method: "DELETE" })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then(() => fetchComments())
      .catch((error) => {
        alert(error);
      });
  };

  const handleEditComment = (comment_id) => {
    fetch(BASE_URL + comment_id)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((data) => {
        setOpenCreateComment(true);
        setUsername(data.username);
        setNewComment(data.censored_text);
        setCommentId(data.id);
      })
      .catch((error) => {
        alert(error);
      });
  };

  const fetchComments = () => {
    fetch(BASE_URL)
      .then((response) => {
        if (response.status === 204) {
          setComments([]);
          return null;
        }
        return response.json();
      })
      .then((data) => {
        if (data === null) {
          setMessage("Ещё нет ни одного комментария");
        } else {
          setComments(data);
        }
      })
      .catch((error) => console.log(error));
  };

  function timeAgo(date) {
    const now = new Date();
    const diffInMs = now.getTime() - new Date(date).getTime();

    const minutes = Math.floor(diffInMs / (1000 * 60));
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    const weeks = Math.floor(days / 7);
    const months = Math.floor(days / 30);
    const years = Math.floor(months / 12);

    if (minutes < 1) return "Только что";
    else if (minutes === 1) return "Минуту назад";
    else if (minutes < 60) return `${minutes} мин. назад`;
    else if (hours === 1) return "Час назад";
    else if (hours < 24) return `${hours} ч. назад`;
    else if (days === 1) return "День назад";
    else if (days < 7) return `${days} дня назад`;
    else if (weeks === 1) return "Неделю назад";
    else if (months === 1) return "Месяц назад";
    else if (years === 1) return "Год назад";
    else return `${years} лет назад`;
  }

  return (
    <>
      <Modal
        open={openCreateComment}
        onClose={() => {
          setOpenCreateComment(false);
          setCommentId(0);
          setUsername("");
          setNewComment("");
        }}
      >
        <div className="create-comment-modal">
          <form className="comment-form">
            <input
              className="comment-form__input"
              type="text"
              placeholder="Напишите ваше имя"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            <textarea
              className="comment-form__textarea"
              type="text"
              placeholder="Напишите комментарий"
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
            />
            <button
              className="comment-form__button"
              type="submit"
              disabled={!newComment || !username}
              onClick={publishComment}
            >
              <svg
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                fill="#000000"
              >
                <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                <g
                  id="SVGRepo_tracerCarrier"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                ></g>
                <g id="SVGRepo_iconCarrier">
                  {" "}
                  <rect x="0" fill="none" width="24" height="24"></rect>{" "}
                  <g>
                    {" "}
                    <path d="M21 14v5c0 1.105-.895 2-2 2H5c-1.105 0-2-.895-2-2V5c0-1.105.895-2 2-2h5v2H5v14h14v-5h2z"></path>{" "}
                    <path d="M21 7h-4V3h-2v4h-4v2h4v4h2V9h4"></path>{" "}
                  </g>{" "}
                </g>
              </svg>
              Опубликовать
            </button>
          </form>
        </div>
      </Modal>
      <div className="header">
        <div className="header__title">
          <h1>неТоксичные комментарии</h1>
        </div>
        <div className="header__my-links">
          <a target="_blank" href="https://github.com/IvanZaycev0717/">
            <img src="./src/assets/github.svg" alt="" />
          </a>
          <a target="_blank" href="https://telegram.me/ivanzaycev0717">
            <img src="./src/assets/telegram.svg" alt="" />
          </a>
        </div>
      </div>
      <div className="write-comment-container">
        <button
          className="write-comment-container__button"
          onClick={() => setOpenCreateComment(true)}
        >
          <svg
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            fill="#000000"
          >
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g
              id="SVGRepo_tracerCarrier"
              stroke-linecap="round"
              stroke-linejoin="round"
            ></g>
            <g id="SVGRepo_iconCarrier">
              {" "}
              <rect x="0" fill="none" width="24" height="24"></rect>{" "}
              <g>
                {" "}
                <path d="M21 14v5c0 1.105-.895 2-2 2H5c-1.105 0-2-.895-2-2V5c0-1.105.895-2 2-2h5v2H5v14h14v-5h2z"></path>{" "}
                <path d="M21 7h-4V3h-2v4h-4v2h4v4h2V9h4"></path>{" "}
              </g>{" "}
            </g>
          </svg>
          Написать комментарий
        </button>
      </div>
      <div className="comments-container">
        {message}
        {comments.map((comment) => (
          <div className="comment-card" key={comment.id}>
            <p>
              <strong>{comment.username}</strong> • {timeAgo(comment.date)}
            </p>
            <hr></hr>
            <p>{comment.censored_text}</p>
            <div className="comment-card__buttons">
              <button
                className="comment-card__buttons-button"
                onClick={() => handleEditComment(comment.id)}
              >
                <svg
                  viewBox="0 -0.5 21 21"
                  version="1.1"
                  xmlns="http://www.w3.org/2000/svg"
                  xmlns:xlink="http://www.w3.org/1999/xlink"
                  fill="#000000"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    {" "}
                    <title>edit_cover [#1481]</title>{" "}
                    <desc>Created with Sketch.</desc> <defs> </defs>{" "}
                    <g
                      id="Page-1"
                      stroke="none"
                      stroke-width="1"
                      fill="none"
                      fill-rule="evenodd"
                    >
                      {" "}
                      <g
                        id="Dribbble-Light-Preview"
                        transform="translate(-419.000000, -359.000000)"
                        fill="#000000"
                      >
                        {" "}
                        <g
                          id="icons"
                          transform="translate(56.000000, 160.000000)"
                        >
                          {" "}
                          <path
                            d="M384,209.210475 L384,219 L363,219 L363,199.42095 L373.5,199.42095 L373.5,201.378855 L365.1,201.378855 L365.1,217.042095 L381.9,217.042095 L381.9,209.210475 L384,209.210475 Z M370.35,209.51395 L378.7731,201.64513 L380.4048,203.643172 L371.88195,212.147332 L370.35,212.147332 L370.35,209.51395 Z M368.25,214.105237 L372.7818,214.105237 L383.18415,203.64513 L378.8298,199 L368.25,208.687714 L368.25,214.105237 Z"
                            id="edit_cover-[#1481]"
                          >
                            {" "}
                          </path>{" "}
                        </g>{" "}
                      </g>{" "}
                    </g>{" "}
                  </g>
                </svg>
                Редактировать
              </button>
              <button
                className="comment-card__buttons-button"
                onClick={() => handleDeleteComment(comment.id)}
              >
                <svg
                  fill="#000000"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
                  <g
                    id="SVGRepo_tracerCarrier"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  ></g>
                  <g id="SVGRepo_iconCarrier">
                    <path d="M5.755,20.283,4,8H20L18.245,20.283A2,2,0,0,1,16.265,22H7.735A2,2,0,0,1,5.755,20.283ZM21,4H16V3a1,1,0,0,0-1-1H9A1,1,0,0,0,8,3V4H3A1,1,0,0,0,3,6H21a1,1,0,0,0,0-2Z"></path>
                  </g>
                </svg>
                Удалить
              </button>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}

export default App;
