import type { VernacularLanguage } from "@/types";

// Mirrors backend/routers/chat.py VERNACULAR_LANGUAGES — used as a non-blocking fallback so
// the language switcher still renders when the backend is unavailable (static preview).
export const FALLBACK_LANGUAGES: VernacularLanguage[] = [
  { code: "hi", name: "Hindi", native: "हिन्दी" },
  { code: "en", name: "English", native: "English" },
  { code: "bn", name: "Bengali", native: "বাংলা" },
  { code: "te", name: "Telugu", native: "తెలుగు" },
  { code: "mr", name: "Marathi", native: "मराठी" },
  { code: "ta", name: "Tamil", native: "தமிழ்" },
  { code: "gu", name: "Gujarati", native: "ગુજરાતી" },
  { code: "ur", name: "Urdu", native: "اردو" },
  { code: "kn", name: "Kannada", native: "ಕನ್ನಡ" },
  { code: "or", name: "Odia", native: "ଓଡ଼ିଆ" },
  { code: "ml", name: "Malayalam", native: "മലയാളം" },
  { code: "pa", name: "Punjabi", native: "ਪੰਜਾਬੀ" },
  { code: "as", name: "Assamese", native: "অসমীয়া" },
  { code: "mai", name: "Maithili", native: "मैथिली" },
  { code: "sat", name: "Santali", native: "ᱥᱟᱱᱛᱟᱲᱤ" },
  { code: "ks", name: "Kashmiri", native: "कॉशुर" },
  { code: "ne", name: "Nepali", native: "नेपाली" },
  { code: "kok", name: "Konkani", native: "कोंकणी" },
  { code: "doi", name: "Dogri", native: "डोगरी" },
  { code: "sd", name: "Sindhi", native: "सिन्धी" },
  { code: "brx", name: "Bodo", native: "बर'" },
  { code: "sa", name: "Sanskrit", native: "संस्कृतम्" },
  { code: "mni", name: "Manipuri", native: "মণিপুরী" },
];

// Localized greeting shown by Yojana Sahayak when the chat panel opens.
export const CHAT_GREETINGS: Record<string, string> = {
  hi: "नमस्ते! मैं योजना सहायक हूँ। सरकारी योजनाओं की पात्रता, आवश्यक दस्तावेज़ या आवेदन प्रक्रिया के बारे में कुछ भी पूछें।",
  en: "Namaste! I am Yojana Sahayak. Ask me anything about government scheme eligibility, required documents, or how to apply.",
  bn: "নমস্কার! আমি যোজনা সহায়ক। সরকারি প্রকল্পের যোগ্যতা, নথি বা আবেদন প্রক্রিয়া নিয়ে যা খুশি জিজ্ঞাসা করুন।",
  te: "నమస్కారం! నేను యోజన సహాయక్. ప్రభుత్వ పథకాల అర్హత, పత్రాలు లేదా దరఖాస్తు గురించి అడగండి.",
  mr: "नमस्कार! मी योजना सहाय्यक आहे. सरकारी योजनांची पात्रता, कागदपत्रे किंवा अर्ज प्रक्रिया विचारा.",
  ta: "வணக்கம்! நான் யோஜனா சகாயக். அரசு திட்டங்களின் தகுதி, ஆவணங்கள் பற்றி கேளுங்கள்.",
  gu: "નમસ્તે! હું યોજના સહાયક છું. સરકારી યોજનાઓની પાત્રતા કે દસ્તાવેજો વિશે પૂછો.",
  ur: "نمستے! میں یوجنا سہایک ہوں۔ سرکاری اسکیموں کی اہلیت یا دستاویزات کے بارے میں پوچھیں۔",
  kn: "ನಮಸ್ಕಾರ! ನಾನು ಯೋಜನಾ ಸಹಾಯಕ. ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ಅರ್ಹತೆ ಬಗ್ಗೆ ಕೇಳಿ.",
  or: "ନମସ୍କାର! ମୁଁ ଯୋଜନା ସହାୟକ। ସରକାରୀ ଯୋଜନା ବିଷୟରେ ପଚାରନ୍ତୁ।",
  ml: "നമസ്കാരം! ഞാൻ യോജന സഹായക്. സർക്കാർ പദ്ധതികളെക്കുറിച്ച് ചോദിക്കുക.",
  pa: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਯੋਜਨਾ ਸਹਾਇਕ ਹਾਂ। ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਬਾਰੇ ਪੁੱਛੋ।",
  as: "নমস্কাৰ! মই যোজনা সহায়ক। চৰকাৰী আঁচনিৰ বিষয়ে সোধক।",
};

export const SUGGESTED_PROMPTS: Record<string, string[]> = {
  hi: [
    "मेरे लिए कौन सी योजनाएँ सबसे अच्छी हैं?",
    "PM-KISAN के लिए कौन से दस्तावेज़ चाहिए?",
    "आयुष्मान कार्ड कैसे बनवाएँ?",
  ],
  en: [
    "Which schemes suit me best?",
    "What documents do I need for PM-KISAN?",
    "How do I get my Ayushman card?",
  ],
};
