import { Routes, Route } from "react-router-dom";
import { Toaster } from "@/components/ui/sonner";
import Home from "@/pages/Home";
import Questionnaire from "@/pages/Questionnaire";
import Results from "@/pages/Results";
import Report from "@/pages/Report";

// One <Route> per page in src/pages; BrowserRouter already wraps this in main.tsx.
export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/questionnaire" element={<Questionnaire />} />
        <Route path="/results" element={<Results />} />
        <Route path="/report" element={<Report />} />
        <Route path="*" element={<Home />} />
      </Routes>
      <Toaster position="top-center" richColors />
    </>
  );
}
