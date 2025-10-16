import ThemeToggle from './ThemeToggle';

export default function Layout({ children }: { children: React.ReactNode }) {
    return (
      <div className="min-h-screen gradient-bg">
        <ThemeToggle />
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          {/* Header */}
          <header className="text-center mb-12">
            <div className="glass rounded-2xl p-8 mb-8">
              <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-[var(--foreground)] via-[var(--secondary)] to-[var(--primary)] bg-clip-text text-transparent">
                🎨 ChromaCraft
              </h1>
              <p className="text-lg font-medium" style={{ color: 'var(--secondary)' }}>
                AI-Powered Color Palette Extraction & Concept Adjustment
              </p>
            </div>
          </header>

          {/* Main Content */}
          <main className="space-y-8">
            {children}
          </main>

          {/* Footer */}
          <footer className="mt-16 text-center">
            <div className="glass rounded-xl p-6">
              <p className="text-sm" style={{ color: 'var(--secondary)' }}>
                Built with ❤️ using AI • Extract colors, adjust concepts, create magic
              </p>
            </div>
          </footer>
        </div>
      </div>
    );
  }
  