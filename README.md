# 🎨 ChromaCraft

**AI-Powered Color Palette Extraction & Concept-based Generation**

ChromaCraft is a modern web application that uses artificial intelligence to generate beautiful, harmonious color palettes from both images and text concepts. Perfect for designers, artists, and developers who need intelligent color suggestions.

---

## ✨ Features

### 🎯 **Core Features**
- **📸 Image-based Extraction** - Upload images and extract dominant colors
- **🤖 AI Concept Generation** - Generate palettes from text descriptions using OpenAI
- **🎭 Mood Adjustments** - Transform existing palettes based on mood descriptions
- **🎨 Interactive Editing** - Coolors-style palette editor with real-time preview
- **📥 Multiple Export Formats** - PNG, JSON, CSS, and more

### 🔮 **AI-Powered Features**
- **Natural Language Processing** - "Sunset over the ocean", "Cozy autumn cabin"
- **Semantic Mood Matching** - Intelligent color harmony based on emotions
- **Retry Logic** - Robust API handling with exponential backoff
- **Character Validation** - Smart input validation and error handling

---

## 🏗️ **Project Structure**

```
ChromaCraft/
├── 📁 frontend/                   # Next.js 14+ Frontend
│   ├── app/                       # App Router pages
│   ├── components/                # React components
│   │   ├── ConceptPaletteGenerator.tsx  # AI concept input
│   │   ├── ColorSwatch.tsx        # Individual color display
│   │   ├── ImageUploader.tsx      # Image upload handling
│   │   └── PaletteDisplay.tsx     # Palette visualization
│   ├── lib/                       # Utilities & API client
│   │   ├── api-client.ts          # Type-safe API communication
│   │   ├── types.ts               # TypeScript definitions
│   │   └── constants.ts           # App constants
│   └── utils/                     # Frontend utilities
├── 📁 backend/                    # FastAPI Backend
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Environment configuration
│   ├── utils/                     # Backend utilities
│   │   ├── openai_palette_generator.py  # OpenAI integration
│   │   ├── color_extractor.py     # Image processing
│   │   ├── mood_adjuster.py       # AI mood adjustments
│   │   └── color_names.json       # XKCD color database
│   └── tests/                     # Backend tests
├── 📄 package.json                # Root workspace config
├── 📄 pnpm-workspace.yaml         # PNPM workspace
├── 📄 .env.example                # Environment template
├── 📄 TODO.md                     # Development roadmap
└── 📄 dev.bat                     # Quick dev startup
```

---

## 🚀 **Quick Start**

### Prerequisites
- **Node.js** 18+ and **pnpm** 8+
- **Python** 3.8+ 
- **OpenAI API Key** (for concept generation)

### 1️⃣ **Clone & Setup**
```bash
# Clone the repository
git clone https://github.com/IbukunSanni/ChromaCraft.git
cd ChromaCraft

# Install all dependencies (frontend + backend)
pnpm run setup
```

### 2️⃣ **Environment Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_api_key_here
```

### 3️⃣ **Start Development**
```bash
# Start both frontend and backend
pnpm run dev
# or
dev.bat  # Windows users
```

### 🌐 **Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🛠️ **Tech Stack**

### **Frontend**
- **⚡ Next.js 14+** - React framework with App Router
- **🎨 Tailwind CSS** - Utility-first CSS framework
- **📘 TypeScript** - Type-safe JavaScript
- **🔄 React Hooks** - Modern React patterns

### **Backend** 
- **🚀 FastAPI** - Modern Python web framework
- **🤖 OpenAI API** - AI-powered concept generation
- **🧠 Sentence Transformers** - Semantic similarity matching
- **🖼️ ColorThief & Pillow** - Image processing
- **⚡ Uvicorn** - High-performance ASGI server

### **Development Tools**
- **📦 PNPM** - Fast, disk-efficient package manager
- **🔧 Concurrently** - Run multiple dev servers
- **🧪 Jest & Pytest** - Frontend and backend testing
- **🎯 ESLint & Flake8** - Code linting

---

## 📚 **Available Scripts**

| Command | Description |
|---------|-------------|
| `pnpm run dev` | Start both frontend and backend |
| `pnpm run setup` | Install all dependencies |
| `pnpm run build` | Build for production |
| `pnpm run test` | Run all tests |
| `pnpm run lint` | Lint all code |
| `pnpm run clean` | Clean build artifacts |
---

## 🖼️ **Screenshots**

### **AI Concept Generation**
Generate beautiful palettes from natural language:

![Horizon-Zero-Dawn](https://github.com/user-attachments/assets/416c746d-91d9-44dc-abce-a264ce103afd)

### **Application Interface**
Clean, modern interface with real-time preview:

![image](https://github.com/user-attachments/assets/eab8e5e1-f7fe-42f7-8e70-ca7b0c881c82)

---

## 🎯 **Use Cases**

- **🎨 Designers** - Generate mood-based palettes for branding and UI design
- **👨‍🎨 Artists** - Extract colors from inspiration images and create variations
- **💻 Developers** - Generate consistent color schemes for applications
- **📱 Product Teams** - Create cohesive brand color systems
- **🏢 Agencies** - Rapid palette generation for client presentations

---

## 🚀 **Why ChromaCraft?**

ChromaCraft bridges the gap between **human creativity** and **AI intelligence**. Instead of limiting to just picking colors, ChromaCraft:

✨ **Understands Context** - "Cozy autumn cabin" generates warm, earthy tones  
🎭 **Captures Emotions** - Semantic analysis creates mood-appropriate palettes  
⚡ **Works Fast** - Generate dozens of variations in seconds  
🔄 **Stays Consistent** - Maintains harmony across all generated colors  
🎨 **Learns Continuously** - AI improves with usage patterns  

---

## 🛣️ **Roadmap**

See our detailed development roadmap in [TODO.md](./TODO.md)

### **Current Phase** 
- ✅ OpenAI concept generation with retry logic
- ✅ Character validation and error handling
- ✅ Robust API architecture
- 🔄 Interactive palette editor (Coolors-style)
- 🔄 Advanced export formats

### **Upcoming Features**
- 🔮 Custom AI model training
- 🎨 Advanced color harmony algorithms  
- 📊 Usage analytics and insights
- 🔗 Design tool integrations
- 📱 Mobile app development

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test them
4. Commit your changes: `git commit -m 'feat: add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

---

## 📄 **License**

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **OpenAI** - For providing the GPT API that powers concept generation
- **XKCD Color Survey** - For the comprehensive color naming database
- **ColorThief** - For efficient image color extraction
- **FastAPI & Next.js** - For excellent development frameworks

---

<div align="center">

[⭐ Star us on GitHub](https://github.com/IbukunSanni/ChromaCraft) • [🐛 Report Bug](https://github.com/IbukunSanni/ChromaCraft/issues) • [✨ Request Feature](https://github.com/IbukunSanni/ChromaCraft/issues)

</div>




