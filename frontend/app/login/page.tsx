"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const { user, refreshUser } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  if (user) {
    router.push("/");
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    try {
      await login(email, password);
      await refreshUser();
      router.push("/");
    } catch {
      setError("Invalid credentials");
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-black text-white">
      <form
        onSubmit={handleSubmit}
        className="flex flex-col gap-4 w-80"
      >
        <h1 className="text-2xl font-bold">Login</h1>

        <input
          type="email"
          placeholder="Email"
          className="p-2 text-white"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          className="p-2 text-white"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          className="bg-white text-black p-2 font-bold"
        >
          Sign In
        </button>

        <p className="text-sm text-neutral-400 text-center">
          Don’t have an account?{" "}
          <a
            href="/register"
            className="text-white underline hover:text-neutral-300 transition"
          >
            Register
          </a>
        </p>


        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}
      </form>
    </main>
  );
}
