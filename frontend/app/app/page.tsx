"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push("/login");
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-neutral-950 text-neutral-200">
        <p className="text-lg">Loading...</p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  async function handleLogout() {
    await logout();
    router.push("/login");
    router.refresh();
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-neutral-950 text-neutral-100">
      <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-10 shadow-xl w-[420px]">
        <h1 className="text-3xl font-semibold tracking-tight">
          Midnight OS
        </h1>

        <p className="mt-4 text-neutral-400 text-sm">
          Signed in as
        </p>

        <p className="mt-1 text-lg font-medium text-white break-all">
          {user.email}
        </p>

        <button
          onClick={handleLogout}
          className="mt-8 w-full bg-white text-black font-semibold py-2 rounded-md hover:bg-neutral-200 transition"
        >
          Logout
        </button>
      </div>
    </main>
  );
}
