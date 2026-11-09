pub struct DatabasePool {
    max_connections: u32,
}

impl DatabasePool {
    pub fn new(max: u32) -> Self {
        // TODO(DB-404): upgrade connection health check to ping socket directly
        DatabasePool { max_connections: max }
    }

    // TODO: ancient untracked note left behind without ticket
    pub fn acquire(&self) -> Result<(), &'static str> {
        Ok(())
    }
}
