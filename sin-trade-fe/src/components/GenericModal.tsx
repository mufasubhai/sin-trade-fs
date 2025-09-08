/* eslint-disable @typescript-eslint/prefer-nullish-coalescing */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
"use client";

import {
  Dialog,
  DialogBackdrop,
  DialogPanel,
  DialogTitle,
} from "@headlessui/react";

import Button from "../components/AsyncButton";

export default function GenericModal({
  open,
  setOpen,
  title,
  child,
  confirmFunction,
  confirmText,
  // confirmArgs,
  isError,
  isLoading,
  confirmDisabled,
  icon,
}: {
  open: boolean;
  setOpen: (open: boolean) => void;
  title: string;
  // confirmArgs: unknown[] | undefined;
  confirmFunction: () => unknown;
  child: JSX.Element;
  icon: React.ReactElement;
  confirmText: string | undefined;
  confirmDisabled: boolean | undefined;
  isLoading: boolean | undefined;
  isError: boolean | undefined;
}) {
  return (
    <Dialog open={open} onClose={setOpen} className="relative z-10">
      <DialogBackdrop
        transition
        className="fixed inset-0 bg-gray-500/75 transition-opacity data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in"
      />
      <div className="fixed inset-0 z-10 w-screen overflow-y-auto">
        <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
          <DialogPanel
            transition
            className="relative transform overflow-hidden rounded-lg bg-white px-4 pt-5 pb-4 text-left shadow-xl transition-all data-closed:translate-y-4 data-closed:opacity-0 data-enter:duration-300 data-enter:ease-out data-leave:duration-200 data-leave:ease-in sm:my-8 sm:w-full sm:max-w-lg sm:p-6 data-closed:sm:translate-y-0 data-closed:sm:scale-95"
          >
            <div className="flex flex-row min-w-full justify-center">
              <div className="mx-auto flex size-12 shrink-items-center justify-center rounded-full bg-red-100 sm:mx-0 sm:size-10">
                {icon ? icon : <></>}
              </div>
            </div>
            {/* <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left"> */}
            <DialogTitle
              as="h3"
              className="text-base justify-center text-center font-semibold text-gray-900"
            >
              {title}
            </DialogTitle>
            {child}
            {/* </div> */}
            <div className="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
              <Button
                text={confirmText ?? "Confirm"}
                onClick={() => confirmFunction()}
                isError={isError !== undefined ? isError : false}
                disabled={
                  confirmDisabled !== undefined ? confirmDisabled : false
                }
                isLoading={isLoading != undefined ? isLoading : false}
              />
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="inline-flex w-full justify-center rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white shadow-xs hover:bg-red-500 sm:mr-3 sm:w-auto"
              >
                Close
              </button>
            </div>
          </DialogPanel>
        </div>
      </div>
    </Dialog>
  );
}
