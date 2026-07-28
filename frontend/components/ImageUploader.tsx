"use client";

import Image from "next/image";
import { useState } from "react";
import { API_BASE_URL } from "@/lib/constants";

type ImageUploaderProps = {
  onColorExtracted: (colors: string[]) => void;
  onColorNamesExtracted: (names: string[]) => void;
};

export default function ImageUploader({
  onColorExtracted,
  onColorNamesExtracted,
}: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  async function handleFile(file: File) {
    setPreview(URL.createObjectURL(file));
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_BASE_URL}/extract-colors`, {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      onColorNamesExtracted(data.names);
      onColorExtracted(data.colors);
    } catch (err) {
      console.error("Error uploading image:", err);
    } finally {
      setLoading(false);
    }
  }

  async function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    await handleFile(file);
  }

  function handleDrag(e: React.DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }

  async function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith("image/")) {
      await handleFile(file);
    }
  }

  return (
    <div className="card-gradient rounded-2xl p-8">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-3" style={{ color: 'var(--foreground)' }}>
        📸 Upload Your Image
      </h2>

      <input
        id="file-input"
        type="file"
        accept="image/*"
        onChange={handleChange}
        className="hidden"
      />

      <div
        className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 ${
          dragActive
            ? "scale-105"
            : "hover:scale-[1.02]"
        }`}
        style={{
          borderColor: dragActive ? 'var(--primary)' : 'var(--muted)',
          backgroundColor: dragActive ? 'var(--accent)20' : 'transparent'
        }}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {!preview ? (
          <div className="space-y-4">
            <div className="text-6xl">🎨</div>
            <div>
              <p className="text-lg font-medium mb-2" style={{ color: 'var(--foreground)' }}>
                Drop your image here or click to browse
              </p>
              <p className="text-sm" style={{ color: 'var(--secondary)' }}>
                Supports JPG, PNG, GIF up to 10MB
              </p>
            </div>
            <label
              htmlFor="file-input"
              className="inline-block cursor-pointer px-6 py-3 text-white font-medium rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
              style={{ background: `linear-gradient(to right, var(--primary), var(--accent))` }}
            >
              Choose Image
            </label>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="relative inline-block">
              <Image
                src={preview}
                alt="Preview"
                width={300}
                height={300}
                className="rounded-xl shadow-lg max-w-full h-auto"
              />
              {loading && (
                <div className="absolute inset-0 bg-black/50 rounded-xl flex items-center justify-center">
                  <div className="text-white text-center">
                    <div className="animate-spin w-8 h-8 border-4 border-white border-t-transparent rounded-full mx-auto mb-2"></div>
                    <p className="text-sm">Extracting colors...</p>
                  </div>
                </div>
              )}
            </div>
            <label
              htmlFor="file-input"
              className="inline-block cursor-pointer px-4 py-2 text-white rounded-lg transition-colors duration-300 hover:opacity-80"
              style={{ backgroundColor: 'var(--secondary)' }}
            >
              Choose Different Image
            </label>
          </div>
        )}
      </div>
    </div>
  );
}
