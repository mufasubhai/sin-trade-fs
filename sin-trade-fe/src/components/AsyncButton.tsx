export default function AsyncButton({
  text,
  onClick,
  disabled,
  isLoading,
  isError,
}: {
  text: string;
  onClick: () => void;
  disabled: boolean;
  isLoading: boolean;
  isError: boolean;
  // className?: string
}) {
  return (
    // will replace this with a loading spinner
    isLoading ? (
      <div>Loading...</div>
    ) : (
      <button
        type="button"
        className={
          isError
            ? "rounded-md bg-red-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-red-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-600"
            : `rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 ${
                disabled ? "opacity-50 cursor-not-allowed" : ""
              }`
        }
        onClick={onClick}
        disabled={disabled}
      >
        {text}
      </button>
    )
  );
}
