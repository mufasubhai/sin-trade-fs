// "use client";

import { Label } from "../../components/catalyst_components/fieldset";
import {
  Switch,
  SwitchField,
} from "../../components/catalyst_components/switch";
import { useState } from "react";
import Input from "../../components/Input";

import {
  // Dialog,
  // DialogBackdrop,
  // DialogPanel,
  Menu,
  MenuButton,
  MenuItem,
  MenuItems,
  // TransitionChild,
} from "@headlessui/react";
import {
  // Bars3Icon,
  BellIcon,
  CalendarIcon,
  ChartPieIcon,
  // DocumentDuplic/ateIcon,
  // FolderIcon,
  PlusIcon,
  HomeIcon,
  UserCircleIcon,
  // UsersIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import {
  ChevronDownIcon,
  MagnifyingGlassIcon,
} from "@heroicons/react/20/solid";
import { useAuth } from "../../context/useAuth";
import { type AuthContextType } from "../../context/AuthContext";
import GenericModal from "../../components/GenericModal";
import { addAsset } from "../../api/AddAsset";

const navigation = [
  { name: "Dashboard", href: "#", icon: HomeIcon, current: true },
  // { name: "Team", href: "#", icon: UsersIcon, current: false },
  // { name: "Projects", href: "#", icon: FolderIcon, current: false },
  { name: "Calendar", href: "#", icon: CalendarIcon, current: false },
  // { name: "Documents", href: "#", icon: DocumentDuplicateIcon, current: false },
  { name: "Reports", href: "#", icon: ChartPieIcon, current: false },
];

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function Dashboard() {
  const {
    user,
    fetchAssets,
    addAssetToDB,
    assets,
    logoutUser,
  }: AuthContextType = useAuth();

  const userNavigation = [
    // { name: "Your profile" },
    { name: "Sign out", function: () => logoutUser() },
  ];
  // const [sidebarOpen, setSidebarOpen] = useState(false);

  const [searchString, setSearchString] = useState("");
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [assetTicker, setassetTicker] = useState("");
  const [isCrypto, setIsCrypto] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  return (
    <>
      {/*
        This Dashboard requires updating your template:

        ```
        <html class="h-full bg-white">
        <body class="h-full">
        ```
      */}
      <div>
        {/* Static sidebar for desktop */}
        <div className="hidden lg:fixed lg:inset-y-0 lg:left-0 lg:z-50 lg:block lg:w-20 lg:overflow-y-auto lg:bg-gray-900 lg:pb-4">
          <nav className="mt-8">
            <ul role="list" className="flex flex-col items-center space-y-1">
              {navigation.map((item) => (
                <li key={item.name}>
                  <a
                    href={item.href}
                    className={classNames(
                      item.current
                        ? "bg-gray-800 text-white"
                        : "text-gray-400 hover:bg-gray-800 hover:text-white",
                      "group flex gap-x-3 rounded-md p-3 text-sm/6 font-semibold"
                    )}
                  >
                    <item.icon aria-hidden="true" className="size-6 shrink-0" />
                    <span className="sr-only">{item.name}</span>
                  </a>
                </li>
              ))}
            </ul>
          </nav>
        </div>

        <div className="lg:pl-20">
          <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-xs sm:gap-x-6 sm:px-6 lg:px-8">
            {/* Separator */}
            <div
              aria-hidden="true"
              className="h-6 w-px bg-gray-900/10 lg:hidden"
            />

            <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
              <form action="#" method="GET" className="grid flex-1 grid-cols-1">
                <input
                  name="search"
                  type="search"
                  placeholder="Search"
                  aria-label="Search"
                  onChange={(e) => {
                    setSearchString(e.target.value);
                  }}
                  className="col-start-1 row-start-1 block size-full bg-white pl-8 text-base text-gray-900 outline-hidden placeholder:text-gray-400 sm:text-sm/6"
                />
                <MagnifyingGlassIcon
                  aria-hidden="true"
                  className="pointer-events-none col-start-1 row-start-1 size-5 self-center text-gray-400"
                />
              </form>
              <div className="flex items-center gap-x-4 lg:gap-x-6">
                <button
                  type="button"
                  className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500"
                >
                  <span className="sr-only">View notifications</span>
                  <BellIcon aria-hidden="true" className="size-6" />
                </button>

                {/* Separator */}
                <div
                  aria-hidden="true"
                  className="hidden lg:block lg:h-6 lg:w-px lg:bg-gray-900/10"
                />

                {/* Profile dropdown */}
                <Menu as="div" className="relative" data-testid="user-menu">
                  <MenuButton className="-m-1.5 flex items-center p-1.5">
                    <span className="sr-only">Open user menu</span>

                    {user?.avatarUrl ? (
                      <img
                        alt={user.username ?? ""}
                        src={user.avatarUrl ?? ""}
                        className="size-8 rounded-full bg-gray-50"
                      />
                    ) : (
                      <UserCircleIcon
                        aria-hidden="true"
                        className="pointer-events-none col-start-1 row-start-1 size-5 self-center text-gray-400"
                      />
                    )}

                    <span className="hidden lg:flex lg:items-center">
                      <span
                        aria-hidden="true"
                        className="ml-4 text-sm/6 font-semibold text-gray-900"
                      >
                        {user?.firstName + " " + user?.lastName}
                      </span>
                      <ChevronDownIcon
                        aria-hidden="true"
                        className="ml-2 size-5 text-gray-400"
                      />
                    </span>
                  </MenuButton>
                  <MenuItems
                    transition
                    className="absolute right-0 z-10 mt-2.5 w-32 origin-top-right rounded-md bg-white py-2 ring-1 shadow-lg ring-gray-900/5 transition focus:outline-hidden data-closed:scale-95 data-closed:transform data-closed:opacity-0 data-enter:duration-100 data-enter:ease-out data-leave:duration-75 data-leave:ease-in"
                  >
                    {userNavigation.map((item) => (
                      <MenuItem key={item.name}>
                        <div
                          className="block px-3 py-1 text-sm/6 text-gray-900 data-focus:bg-gray-50 data-focus:outline-hidden"
                          onClick={() => {
                            if (item.function) {
                              item.function();
                            }
                          }}
                        >
                          {item.name}
                        </div>
                      </MenuItem>
                    ))}
                  </MenuItems>
                </Menu>
              </div>
            </div>
          </div>

          <main className="xl:pl-12">
            <div className="max-w-96 flex flex-row justify-between">
              <div className="">Current Active Assets</div>
              <div className="">
                <button onClick={() => setAddModalOpen(true)}>Add Asset</button>
              </div>
            </div>

            <GenericModal
              open={isSuccess}
              setOpen={setIsSuccess}
              title="Asset Added"
              child={<div>Asset Added</div>}
              confirmFunction={() => {
                setIsSuccess(false);
              }}
              confirmText="Close"
              confirmDisabled={false}
              isLoading={false}
              isError={false}
              icon={<XMarkIcon />}
            />

            <GenericModal
              open={addModalOpen}
              setOpen={setAddModalOpen}
              title="Add Asset"
              child={
                <AddAssetModalBody
                  assetTicker={assetTicker}
                  setassetTicker={setassetTicker}
                  isCrypto={isCrypto}
                  setIsCrypto={setIsCrypto}
                />
              }
              isLoading={isLoading}
              isError={isError}
              icon={<PlusIcon />}
              confirmFunction={() =>
                // maybe change the structure of this a bit.
                addAsset({
                  assetTicker,
                  isCrypto,
                  fetchAssets,
                  addAssetToDB,
                  setIsLoading,
                  setIsError,
                  setAddModalOpen,
                  setIsSuccess,
                  accessToken: user?.accessToken ?? "",
                  refreshToken: user?.refreshToken ?? "",
                  userId: user?.userId ?? null,
                })
              }
              // make these not mandatory
              confirmText={"Add Asset"}
              confirmDisabled={false}
            />
            <div className="px-4 py-10 sm:px-6 lg:px-8 lg:py-6">
              {Object.values(assets ?? {}).map((asset) => {
                if (
                  searchString &&
                  !asset.tickerName
                    .toLowerCase()
                    .includes(searchString.toLowerCase())
                ) {
                  return null;
                }
                // need to add some additional styling to the asset. This should end up being a column thathas the ticker name, last updated, and a button to remove the asset.
                // we also need to add an updated value to the object in the DB.
                return (
                  <div key={asset.assetId}>
                    <h1>{asset.tickerName}</h1>
                  </div>
                );
              })}
            </div>
          </main>
        </div>
      </div>
    </>
  );
}

const AddAssetModalBody = ({
  assetTicker,
  setassetTicker,
  isCrypto,
  setIsCrypto,
}: {
  assetTicker: string;
  setassetTicker: (assetTicker: string) => void;
  isCrypto: boolean;
  setIsCrypto: (isCrypto: boolean) => void;
}) => {
  return (
    <div className="flex flex-col bg-slate-100 p-5 rounded-md">
      <Input
        label="Code"
        placeholder={assetTicker}
        type="text"
        name="ticker_input"
        id="ticker_input"
        onChange={(e) => setassetTicker(e.target.value)}
      />

      <SwitchField color="blue" className="flex p-2 justify-between">
        <Label className="dark:text-red-500 ">Cryptocurrency?</Label>
        <Switch
          color="red"
          name="is_crypto"
          defaultChecked={isCrypto}
          checked={isCrypto}
          onChange={() => setIsCrypto(!isCrypto)}
        />
      </SwitchField>
    </div>
  );
};

// const addAssetModalFunc = async ([
//   assetTicker,
//   isCrypto,
//   setIsLoading,
//   setIsError,
//   setIsSuccess,
// ]: [
//   assetTicker: string,
//   isCrypto: boolean,
//   setIsLoading: (isLoading: boolean) => void,
//   setIsError: (isError: boolean) => void,
//   setIsSuccess: (isSuccess: boolean) => void
// ]) => {
//   await addAsset({
//     assetTicker,
//     isCrypto,
//     setIsLoading,
//     setIsError,
//     setIsSuccess,
//   });
// };
