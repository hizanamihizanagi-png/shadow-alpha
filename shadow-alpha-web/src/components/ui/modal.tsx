"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";

import { cn } from "@/lib/utils";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: React.ReactNode;
  children: React.ReactNode;
  className?: string;
  preventClose?: boolean;
}

export function Modal({
  isOpen,
  onClose,
  title,
  children,
  className,
  preventClose = false,
}: ModalProps) {
  // Prevent body scroll when modal is open
  React.useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget && !preventClose) {
      onClose();
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 bg-black/80 backdrop-blur-sm"
            onClick={handleBackdropClick}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={{ duration: 0.3, type: "spring", bounce: 0.25 }}
            className={cn(
              "glass-panel-heavy relative z-50 w-full max-w-lg overflow-hidden rounded-xl bg-background p-6 shadow-2xl sm:rounded-2xl border border-border",
              className,
            )}
            role="dialog"
            aria-modal="true"
          >
            {title && (
              <div className="mb-4 pr-6">
                <h2 className="text-xl font-semibold font-display">{title}</h2>
              </div>
            )}

            {!preventClose && (
              <button
                onClick={onClose}
                className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                aria-label="Close"
              >
                <X className="h-4 w-4" />
              </button>
            )}

            <div className="relative">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
