import React, { useEffect, useState } from "react";
import Pagination from "../components/Pagination"
import ListQuestions from "../components/ListQuestions"

function RecentQuestions() {
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/questions")
      .then((response) => response.json())
      .then((data) => {
        setQuestions(data.items);
      })
      .catch((error) => {
        console.error("Error getting list of questions:", error);
      });
  }, []);

  return (
    <div>
      <header className="bg-color2 py-4 px-6">
        <div className="container mx-auto">
          <h1 className="text-white text-2xl font-semibold">Recent Questions</h1>
          <p className="text-white text-sm mt-1">
            The latest questions on QuestHub</p>
        </div>
      </header>

      <main>
        <ListQuestions questions={questions} />
      </main>

      {/* 
            <div className="flex justify-center justify-items-center my-2">
                <Pagination />
            </div>
            */}

    </div>
  );
}

export default RecentQuestions;



/*

import { useEffect, useState } from "react";

function RecentQuestions() {
  const [recentQuestions, setRecentQuestions] = useState([]);

  useEffect(() => {
    // Aquí puedes hacer una solicitud a la API para obtener las preguntas recientes
    // Puedes usar fetch o Axios, según tu preferencia
    // Luego, actualiza el estado recentQuestions con los datos recibidos
  }, []);

  return (
    <div>
      <h2>Preguntas Recientes</h2>
      <ul>
        {recentQuestions.map((question) => (
          <li key={question.id}>{question.title}</li>
        ))}
      </ul>
    </div>
  );
}

export default RecentQuestions;

*/