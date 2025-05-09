const API_URL = "http://127.0.0.1:5000/chat";

export async function chatUser(userData) {
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });
        console.log("Response:", response);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error registering user:", error);
        throw error;
    }
}