'use client';
import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { MenuToggleIcon } from '@/components/ui/menu-toggle-icon';
import { createPortal } from 'react-dom';
import { Brain, BarChart3, Search, MessageSquare, ChevronDown } from 'lucide-react';
import { useApp } from '@/lib/context';

const TICKERS = ["AAPL", "TSLA", "NVDA", "BTC-USD", "SPY", "GOOGL", "AMZN", "META"];

const NAV_ITEMS = [
	{ href: '/', label: 'Dashboard', icon: BarChart3 },
	{ href: '/market', label: 'Market', icon: Search },
	{ href: '/social', label: 'Social', icon: MessageSquare },
	{ href: '/coach', label: 'Coach', icon: Brain },
];

export function Header() {
	const [open, setOpen] = React.useState(false);
	const scrolled = useScroll(10);
	const pathname = usePathname();
	const { ticker, setTicker, initialized } = useApp();

	React.useEffect(() => {
		if (open) {
			document.body.style.overflow = 'hidden';
		} else {
			document.body.style.overflow = '';
		}
		return () => {
			document.body.style.overflow = '';
		};
	}, [open]);

	return (
		<header
			className={cn('sticky top-0 z-50 w-full border-b border-transparent transition-all duration-300', {
				'bg-background/80 supports-[backdrop-filter]:bg-background/60 border-border/50 backdrop-blur-2xl shadow-lg shadow-black/5':
					scrolled,
			})}
		>
			<nav className="mx-auto flex h-16 w-full max-w-7xl items-center justify-between px-6">
				{/* Logo */}
				<Link href="/" className="group flex items-center gap-3">
					<div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600 shadow-lg shadow-primary/25 transition-transform group-hover:scale-105">
						<Brain className="h-5 w-5 text-white" />
					</div>
					<div className="hidden sm:block">
						<span className="font-bold text-white">Antifragile</span>
						<span className="ml-1 font-light text-white/60">Mirror</span>
					</div>
				</Link>

				{/* Desktop Navigation */}
				<div className="hidden lg:flex items-center gap-1 rounded-2xl bg-white/[0.03] p-1.5 border border-white/[0.06]">
					{NAV_ITEMS.map((item) => {
						const Icon = item.icon;
						const isActive = pathname === item.href;
						return (
							<Link
								key={item.href}
								href={item.href}
								className={cn(
									"flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-all duration-200",
									isActive
										? "bg-gradient-to-br from-primary/20 to-purple-600/20 text-white shadow-lg shadow-primary/10"
										: "text-white/50 hover:bg-white/[0.05] hover:text-white"
								)}
							>
								<Icon className={cn("h-4 w-4", isActive && "text-primary")} />
								<span>{item.label}</span>
							</Link>
						);
					})}
				</div>
				
				{/* Right Side Controls */}
				<div className="hidden lg:flex items-center gap-4">
					{/* Ticker Selector */}
					<div className="relative">
						<select
							value={ticker}
							onChange={(e) => setTicker(e.target.value)}
							className="appearance-none rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-2.5 pr-10 text-sm font-medium text-white backdrop-blur-sm transition-all focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/20"
						>
							{TICKERS.map((t) => (
								<option key={t} value={t} className="bg-[#1a1225] text-white">
									{t}
								</option>
							))}
						</select>
						<ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-white/40" />
					</div>
					
					{/* Status Badge */}
					<div
						className={cn(
							"flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-medium transition-all",
							initialized
								? "border border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
								: "border border-amber-500/20 bg-amber-500/10 text-amber-400"
						)}
					>
						<span
							className={cn(
								"h-2 w-2 rounded-full",
								initialized ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
							)}
						/>
						<span>{initialized ? "Active" : "Setup"}</span>
					</div>
					
					<Button className="bg-gradient-to-r from-primary to-purple-600 hover:opacity-90 shadow-lg shadow-primary/20">
						Get Started
					</Button>
				</div>
				
				{/* Mobile Menu Toggle */}
				<Button
					size="icon"
					variant="outline"
					onClick={() => setOpen(!open)}
					className="border-white/10 bg-white/[0.03] lg:hidden"
					aria-expanded={open}
					aria-label="Toggle menu"
				>
					<MenuToggleIcon open={open} className="size-5 text-white" duration={300} />
				</Button>
			</nav>
			
			{/* Mobile Menu */}
			<MobileMenu open={open}>
				<div className="flex flex-col gap-2 mb-6">
					{NAV_ITEMS.map((item) => {
						const Icon = item.icon;
						const isActive = pathname === item.href;
						return (
							<Link
								key={item.href}
								href={item.href}
								onClick={() => setOpen(false)}
								className={cn(
									'flex items-center gap-3 rounded-xl p-4 transition-all',
									isActive 
										? 'bg-primary/20 border border-primary/30' 
										: 'hover:bg-white/[0.05] border border-transparent'
								)}
							>
								<div className={cn(
									"flex h-10 w-10 items-center justify-center rounded-lg border",
									isActive ? "bg-primary/20 border-primary/30" : "bg-white/[0.03] border-white/10"
								)}>
									<Icon className={cn("h-5 w-5", isActive ? "text-primary" : "text-white/70")} />
								</div>
								<span className={cn("font-medium", isActive ? "text-white" : "text-white/80")}>
									{item.label}
								</span>
							</Link>
						);
					})}
				</div>
				
				{/* Mobile Ticker Selector */}
				<div className="mb-6">
					<span className="text-xs font-semibold uppercase tracking-wider text-white/40 mb-2 block">
						Select Ticker
					</span>
					<select
						value={ticker}
						onChange={(e) => setTicker(e.target.value)}
						className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-white focus:border-primary/50 focus:outline-none"
					>
						{TICKERS.map((t) => (
							<option key={t} value={t} className="bg-[#1a1225]">
								{t}
							</option>
						))}
					</select>
				</div>
				
				<div className="mt-auto pt-4 border-t border-white/10">
					<Button className="w-full bg-gradient-to-r from-primary to-purple-600">
						Get Started
					</Button>
				</div>
			</MobileMenu>
		</header>
	);
}

function MobileMenu({ open, children }: { open: boolean; children: React.ReactNode }) {
	const [mounted, setMounted] = React.useState(false);
	
	React.useEffect(() => {
		setMounted(true);
	}, []);
	
	if (!open || !mounted) return null;

	return createPortal(
		<div
			className={cn(
				'bg-background/95 supports-[backdrop-filter]:bg-background/80 backdrop-blur-2xl',
				'fixed top-16 right-0 bottom-0 left-0 z-40 flex flex-col overflow-hidden border-t border-white/10 lg:hidden',
			)}
		>
			<div className="size-full p-6 flex flex-col animate-in fade-in-0 slide-in-from-top-2 duration-200">
				{children}
			</div>
		</div>,
		document.body,
	);
}

function useScroll(threshold: number) {
	const [scrolled, setScrolled] = React.useState(false);

	const onScroll = React.useCallback(() => {
		setScrolled(window.scrollY > threshold);
	}, [threshold]);

	React.useEffect(() => {
		window.addEventListener('scroll', onScroll);
		return () => window.removeEventListener('scroll', onScroll);
	}, [onScroll]);

	React.useEffect(() => {
		onScroll();
	}, [onScroll]);

	return scrolled;
}
