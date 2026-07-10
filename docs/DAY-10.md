# Day 10 – React Frontend Setup & Client-Side Routing

## ✅ Completed

Initialized the **Scanly React frontend** and set up the foundation for the user interface using **React Router**, **Axios**, and **Tailwind CSS**.

## Features Added

### 📌 React Router Integration

Configured client-side routing to enable seamless navigation without full page reloads.

Available routes:

* `/` → Home
* `/results` → Scan Results
* `/history` → Scan History

### 📌 Frontend Pages

Created the initial page structure:

* `Home.jsx`
* `Results.jsx`
* `History.jsx`

These pages will be expanded in upcoming development stages.

### 📌 Navbar Component

Implemented a reusable navigation bar to allow users to move between pages while maintaining a consistent application layout.

### 📌 Tailwind CSS Setup

Integrated Tailwind CSS with the Vite React project for rapid, utility-first UI development.

### 📌 Axios Installation

Installed Axios to enable communication between the React frontend and the FastAPI backend for future API integration.

## Folder Structure

```text id="uvj6w5"
scanly-frontend/
├── src/
│   ├── components/
│   │   └── Navbar.jsx
│   │
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Results.jsx
│   │   └── History.jsx
│   │
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
│
├── package.json
└── vite.config.js
```

## Client-Side Routing

Unlike traditional websites that request a new HTML page from the server for every navigation, React uses **client-side routing**.

When users navigate between routes:

* The browser does **not** reload the page.
* React Router updates the URL.
* React renders the appropriate page component.
* Shared components such as the Navbar remain visible, providing a faster and smoother user experience.

## Technologies Used

* React
* Vite
* React Router DOM
* Axios
* Tailwind CSS

## Learning Outcomes

* React project structure
* Client-side routing
* React Router configuration
* Reusable component creation
* Tailwind CSS integration
* API preparation using Axios

## Project Status

### ✅ Frontend Foundation Completed

The Scanly frontend now includes:

* React application setup
* Client-side routing
* Shared navigation component
* Basic page structure
* Tailwind CSS configuration
* Axios for backend communication

**Next:** Day 11 – Connect the frontend with the FastAPI backend, implement the scan form, call the `/scan` API, and display real-time scam detection results.
