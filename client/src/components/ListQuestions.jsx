import {
  List,
  ListItem,
  ListItemPrefix,
  ListItemSuffix,
  Card,
  Typography,
  Chip,
} from "@material-tailwind/react";
import { formatDistanceToNow } from "date-fns";
import { useEffect, useState } from "react"; // Importa useEffect y useState

async function getUsernameById(userId) {
  try {
    const response = await fetch(`http://localhost:8000/users/${userId}/username`);
    if (!response.ok) {
      throw new Error("Error getting username.");
    }
    const data = await response.json();
    return data.username;
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}

export default function ListQuestions({ questions }) {
  const [usernames, setUsernames] = useState({});

  useEffect(() => {
    // Obtener los nombres de usuario para cada pregunta
    const fetchUsernames = async () => {
      const usernamesMap = {};
      for (const question of questions) {
        const username = await getUsernameById(question.author_id);
        console.log(username)
        console.log(username)
        console.log(username)
        console.log(username)
        usernamesMap[question.author_id] = username;
      }
      setUsernames(usernamesMap);
    };

    fetchUsernames();
  }, [questions]);

  return (
    <Card className="w-full overflow-hidden rounded-md">
      <List className="my-2 p-0">
        {questions.map((question, index) => (
          <ListItem className="group rounded-none py-1.5 px-3 text-sm font-normal text-blue-gray-700 hover:bg-color3 hover:text-white focus:bg-color4 focus:text-white" key={index}>
            <ListItemPrefix>
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
              </svg>
            </ListItemPrefix>

            <div>
              <Typography variant="h6" color="blue-gray">
                {question.title}
              </Typography>
              <div className="flex">
                <Chip size="md" color="green" value={question.tag} />
                <div className="w-100"></div>
              </div>
            </div>

            <ListItemSuffix>
              <Typography variant="small" color="gray" className="font-normal ml-auto">
                @{usernames[question.author_id]}
              </Typography>

              <Typography variant="small" color="gray" className="font-normal">
                {formatDistanceToNow(new Date(question.created_at))} ago
              </Typography>
            </ListItemSuffix>
          </ListItem>
        ))}
      </List>
    </Card>
  );
}