# Standard UI Layout Snippets

### 1. Page Header (Modern Glassmorphism)

```tsx
<div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-2 border-b border-border/60">
    <div className="flex items-start gap-4 flex-1">
        <Link to="/previous-page" className="mt-1">
            <Button variant="ghost" size="icon" className="h-10 w-10 rounded-xl hover:bg-muted text-muted-foreground hover:text-primary transition-all border border-transparent hover:border-border">
                <ArrowLeft className="w-5 h-5" />
            </Button>
        </Link>
        <div className="flex flex-col gap-0.5 flex-1 group">
            <div className="flex items-center gap-2.5">
                <Badge variant="outline" className="text-[10px] font-black px-2 py-0.5 uppercase tracking-wider bg-primary/10 text-primary border-primary/20">
                    STATUS
                </Badge>
                <span className="text-[10px] font-medium uppercase tracking-widest text-muted-foreground/30 font-data">
                    ID: #123
                </span>
            </div>
            <h1 className="text-2xl font-bold text-foreground tracking-tight">Main Title</h1>
        </div>
    </div>
    <div className="flex items-center gap-2 bg-muted/20 p-1 rounded-xl border border-border/40 shadow-sm">
        <Button variant="ghost" size="sm" className="h-9 font-semibold text-muted-foreground rounded-lg px-3.5">Secondary Action</Button>
        <div className="w-px h-5 bg-border/40 mx-1" />
        <Button className="bg-primary hover:bg-primary/90 text-primary-foreground font-black h-9 rounded-lg px-5 shadow-lg shadow-primary/10 transition-all hover:scale-[1.02]">
            PRIMARY ACTION
        </Button>
    </div>
</div>
```

### 2. Standard Tabs Navigation

```tsx
<Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
    <div className="sticky top-[-16px] z-20 bg-background/95 backdrop-blur-md border-b border-border -mx-8 px-8 pt-4">
        <TabsList className="bg-transparent h-auto p-0 flex justify-start gap-8">
            {["overview", "details", "pricing"].map((tab) => (
                <TabsTrigger
                    key={tab}
                    value={tab}
                    className="bg-transparent border-none p-0 pb-4 text-[11px] font-semibold uppercase tracking-[0.2em] text-muted-foreground data-[state=active]:text-primary data-[state=active]:after:scale-x-100 relative after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-primary after:scale-x-0 after:transition-transform"
                >
                    {tab}
                </TabsTrigger>
            ))}
        </TabsList>
    </div>
</Tabs>
```

### 3. Loading State (ERP Style)

```tsx
<div className="flex flex-col items-center justify-center min-h-[400px] gap-3 text-muted-foreground">
    <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
    <span className="text-xs font-bold uppercase tracking-widest">Loading Data...</span>
</div>
```
